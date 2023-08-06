import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

import jax
import optax
from datasets import Dataset, DatasetDict, load_dataset, load_from_disk
from flax import jax_utils, traverse_util
from flax.training import train_state
from flax.training.common_utils import get_metrics, onehot, shard
from jax import numpy as jnp
from omegaconf import MISSING
from tqdm import tqdm
from transformers import (
    CONFIG_MAPPING,
    FlaxT5ForConditionalGeneration,
    IntervalStrategy,
    SchedulerType,
    T5Config,
    T5TokenizerFast,
    TrainingArguments,
    is_tensorboard_available,
    set_seed,
)

from git_t5.data import DataCollatorForT5MLM


@dataclass
class ModelConfig:
    model_path: Optional[str] = None
    model_type: Optional[str] = None
    config_path: Optional[str] = None
    tokenizer_path: Optional[str] = None
    cache_dir: Optional[str] = None
    use_fast_tokenizer: bool = True
    dtype: str = "float32"


@dataclass
class DataConfig:
    dataset_name: Optional[str] = None
    dataset_config_name: Optional[str] = None
    dataset_path: Optional[str] = None
    overwrite_cache: bool = False
    val_split_size: float = 0.05
    max_length: Optional[int] = None
    preprocessing_num_workers: Optional[int] = None
    mlm_probability: float = 0.15
    mean_noise_span_length: float = 3.0


@dataclass
class TrainingConfig(TrainingArguments):
    output_dir: str = MISSING
    eval_steps: Optional[int] = None
    evaluation_strategy: IntervalStrategy = IntervalStrategy.NO
    lr_scheduler_type: SchedulerType = SchedulerType.LINEAR
    logging_strategy: IntervalStrategy = IntervalStrategy.STEPS
    save_strategy: IntervalStrategy = IntervalStrategy.STEPS
    push_to_hub_model_id: Optional[str] = None
    push_to_hub_organization: Optional[str] = None
    push_to_hub_token: Optional[str] = None


def compute_input_and_target_lengths(
    inputs_length: int,
    noise_density: float,
    mean_noise_span_length: float,
) -> Tuple[int, int]:
    """This function is copy of `random_spans_helper <https://github.com/google-research/text-to-text-transfer-transformer/blob/84f8bcc14b5f2c03de51bd3587609ba8f6bbd1cd/t5/data/preprocessors.py#L2466>`__ .
    Training parameters to avoid padding with random_spans_noise_mask.
    When training a model with random_spans_noise_mask, we would like to set the other
    training hyperparmeters in a way that avoids padding.
    This function helps us compute these hyperparameters.
    We assume that each noise span in the input is replaced by extra_tokens_per_span_inputs sentinel tokens,
    and each non-noise span in the targets is replaced by extra_tokens_per_span_targets sentinel tokens.
    This function tells us the required number of tokens in the raw example (for split_tokens())
    as well as the length of the encoded targets. Note that this function assumes
    the inputs and targets will have EOS appended and includes that in the reported length.
    Args:
        inputs_length: an integer - desired length of the tokenized inputs sequence
        noise_density: a float
        mean_noise_span_length: a float
    Returns:
        tokens_length: length of original text in tokens
        targets_length: an integer - length in tokens of encoded targets sequence
    """

    def _tokens_length_to_inputs_length_targets_length(
        tokens_length: int,
    ) -> Tuple[int, int]:
        num_noise_tokens = int(round(tokens_length * noise_density))
        num_nonnoise_tokens = tokens_length - num_noise_tokens
        num_noise_spans = int(round(num_noise_tokens / mean_noise_span_length))
        # inputs contain all nonnoise tokens, sentinels for all noise spans
        # and one EOS token.
        _input_length = num_nonnoise_tokens + num_noise_spans + 1
        _output_length = num_noise_tokens + num_noise_spans + 1
        return _input_length, _output_length

    tokens_length = inputs_length

    while (
        _tokens_length_to_inputs_length_targets_length(tokens_length + 1)[0]
        <= inputs_length
    ):
        tokens_length += 1

    inputs_length, targets_length = _tokens_length_to_inputs_length_targets_length(
        tokens_length
    )

    # minor hack to get the targets length to be equal to inputs length
    # which is more likely to have been set to a nice round number.
    if noise_density == 0.5 and targets_length > inputs_length:
        tokens_length -= 1
        targets_length -= 1
    return tokens_length, targets_length


def tokenize_fn(
    tokenizer: T5TokenizerFast,
    text_column_name: str,
) -> Callable[..., Dict[str, Any]]:
    def wrap_fn(examples: Dict[str, Any]) -> Dict[str, Any]:
        return tokenizer(examples[text_column_name], return_attention_mask=False)  # type: ignore

    return wrap_fn


def group_texts(inputs_length: int) -> Callable[..., Dict[str, Any]]:
    def wrap_fn(examples: Dict[str, Any]) -> Dict[str, Any]:
        # Concatenate all texts.
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
        if total_length >= inputs_length:
            total_length = (total_length // inputs_length) * inputs_length
        # Split by chunks of max_len.
        result = {
            k: [t[i : i + inputs_length] for i in range(0, total_length, inputs_length)]
            for k, t in concatenated_examples.items()
        }
        return result

    return wrap_fn


def generate_batch_splits(samples_idx: jnp.ndarray, batch_size: int) -> jnp.ndarray:
    num_samples = len(samples_idx)
    samples_to_remove = num_samples % batch_size
    if samples_to_remove != 0:
        samples_idx = samples_idx[:-samples_to_remove]
    sections_split = num_samples // batch_size
    batch_idx = jnp.split(samples_idx, sections_split)
    return batch_idx


def write_train_metric(summary_writer, train_metrics, train_time, step):
    summary_writer.scalar("train_time", train_time, step)
    train_metrics = get_metrics(train_metrics)
    for key, vals in train_metrics.items():
        tag = f"train_{key}"
        for i, val in enumerate(vals):
            summary_writer.scalar(tag, val, step - len(vals) + i + 1)


def write_eval_metric(summary_writer, eval_metrics, step):
    for metric_name, value in eval_metrics.items():
        summary_writer.scalar(f"eval_{metric_name}", value, step)


class T5Trainer:
    logger: logging.Logger
    datasets: DatasetDict
    tokenizer: T5TokenizerFast
    model: FlaxT5ForConditionalGeneration
    max_length: int
    inputs_length: int
    targets_length: int
    rng: jnp.ndarray

    def __init__(
        self,
        training_config: TrainingConfig,
        model_config: ModelConfig,
        data_config: DataConfig,
    ) -> None:
        self.training_config = training_config
        self.model_config = model_config
        self.data_config = data_config

    def setup(self) -> None:
        # Set the verbosity to info of the Transformers logger (on main process only)
        self.logger = self._get_logger()
        self.logger.info("Training/evaluation parameters %s", self.training_config)

        # Set seed before initializing model.
        set_seed(self.training_config.seed)

        self.setup_tokenizer()
        self.setup_data()
        self.setup_model()

        # T5-like span masked language modeling will fuse consecutively masked tokens to a single sentinel token.
        # To ensure that the input length is `max_seq_length`, we need to increase the maximum length
        # according to `mlm_probability` and `mean_noise_span_length`. We can also define the label length accordingly.
        self.max_length = min(
            self.data_config.max_length,
            self.tokenizer.model_max_length,
        )
        self.inputs_length, self.targets_length = compute_input_and_target_lengths(
            inputs_length=self.max_length,
            noise_density=self.data_config.mlm_probability,
            mean_noise_span_length=self.data_config.mean_noise_span_length,
        )

        self.rng = jax.random.PRNGKey(self.training_config.seed)

    def setup_tokenizer(self) -> None:
        if self.model_config.tokenizer_path:
            tokenizer = T5TokenizerFast.from_pretrained(
                self.model_config.tokenizer_path,
                cache_dir=self.model_config.cache_dir,
                use_fast=self.model_config.use_fast_tokenizer,
            )
        elif self.model_config.model_path:
            tokenizer = T5TokenizerFast.from_pretrained(
                self.model_config.model_path,
                cache_dir=self.model_config.cache_dir,
                use_fast=self.model_config.use_fast_tokenizer,
            )
        else:
            raise ValueError(
                "You are instantiating a new tokenizer from scratch. This is not supported by this script."
                "You can do it from another script, save it, and load it from here, using --tokenizer_name."
            )

        self.tokenizer = tokenizer

    def setup_model(self) -> None:
        assert self.tokenizer is not None
        if self.model_config.config_path is not None:
            config = T5Config.from_pretrained(
                self.model_config.config_path,
                cache_dir=self.model_config.cache_dir,
                vocab_size=len(self.tokenizer),
            )
        elif self.model_config.model_path is not None:
            config = T5Config.from_pretrained(
                self.model_config.model_path,
                cache_dir=self.model_config.cache_dir,
                vocab_size=len(self.tokenizer),
            )
        else:
            config = CONFIG_MAPPING[self.model_config.model_type]()  # type: ignore
            self.logger.warning(
                "You are instantiating a new config instance from scratch."
            )

        assert isinstance(config, T5Config)
        if self.model_config.model_path:
            model = FlaxT5ForConditionalGeneration.from_pretrained(
                self.model_config.model_path,
                config=config,
                seed=self.training_config.seed,
                dtype=getattr(jnp, self.model_config.dtype),
            )
        else:
            model = FlaxT5ForConditionalGeneration(
                config,
                seed=self.training_config.seed,
                dtype=getattr(jnp, self.model_config.dtype),
            )

        self.model = model

    def setup_data(self) -> None:
        if self.data_config.dataset_name is not None:
            # Downloading and loading a dataset from the hub.
            datasets = load_dataset(
                self.data_config.dataset_name,
                self.data_config.dataset_config_name,
                cache_dir=self.model_config.cache_dir,
            )
        elif self.data_config.dataset_path is not None:
            # Loading a dataset from the local disk.
            assert self.data_config.dataset_path is not None
            datasets = load_from_disk(self.data_config.dataset_path)
        else:
            raise ValueError("Need either a dataset name or a local dataset path.")

        if isinstance(datasets, Dataset):
            datasets = datasets.train_test_split(
                test_size=self.data_config.val_split_size
            )
        elif isinstance(datasets, DatasetDict) and "test" in datasets.keys():
            datasets = datasets["train"].train_test_split(
                test_size=self.data_config.val_split_size
            )

        assert isinstance(datasets, DatasetDict)
        self.datasets = datasets

    def preprocess_data(self) -> DatasetDict:
        if self.training_config.do_train:
            column_names = self.datasets["train"].column_names
        else:
            column_names = self.datasets["train"].column_names

        text_column_name = "text" if "text" in column_names else column_names[0]
        tokenized_datasets = self.datasets.map(
            tokenize_fn(self.tokenizer, text_column_name),
            batched=True,
            num_proc=self.data_config.preprocessing_num_workers,
            remove_columns=column_names,
            load_from_cache_file=not self.data_config.overwrite_cache,
        )
        tokenized_datasets = tokenized_datasets.map(
            group_texts(self.inputs_length),
            batched=True,
            num_proc=self.data_config.preprocessing_num_workers,
            load_from_cache_file=not self.data_config.overwrite_cache,
        )

        return tokenized_datasets

    # TODO: Re-write this huge method
    def fit(self) -> None:
        self._check_output_dir_is_empty()

        # Enable tensorboard only on the master node
        summary_writer: Optional[Any] = None
        if is_tensorboard_available() and jax.process_index() == 0:
            try:
                from flax.metrics.tensorboard import SummaryWriter

                summary_writer = SummaryWriter(
                    log_dir=Path(self.training_config.output_dir)
                )
            except ImportError as err:
                self.logger.warning(
                    "Unable to display metrics through TensorBoard because some package are not installed: %s",
                    err,
                )
        else:
            self.logger.warning(
                "Unable to display metrics through TensorBoard because the package is not installed: "
                "Please run pip install tensorboard to enable."
            )

        dropout_rngs = jax.random.split(self.rng, jax.local_device_count())

        tokenized_datasets = self.preprocess_data()

        data_collator = FlaxDataCollatorForT5MLM(
            tokenizer=self.tokenizer,
            noise_density=self.data_config.mlm_probability,
            mean_noise_span_length=self.data_config.mean_noise_span_length,
            input_length=self.max_length,
            target_length=self.targets_length,
            pad_token_id=self.model.config.pad_token_id,
            decoder_start_token_id=self.model.config.decoder_start_token_id,
        )  # type: ignore

        # Store some constant
        num_epochs = int(self.training_config.num_train_epochs)
        train_batch_size = (
            int(self.training_config.per_device_train_batch_size) * jax.device_count()
        )
        eval_batch_size = (
            int(self.training_config.per_device_eval_batch_size) * jax.device_count()
        )
        num_train_steps = (
            len(tokenized_datasets["train"]) // train_batch_size * num_epochs
        )

        # Create learning rate schedule
        warmup_fn = optax.linear_schedule(
            init_value=0.0,
            end_value=self.training_config.learning_rate,
            transition_steps=self.training_config.warmup_steps,
        )
        decay_fn = optax.linear_schedule(
            init_value=self.training_config.learning_rate,
            end_value=0,
            transition_steps=num_train_steps - self.training_config.warmup_steps,
        )
        linear_decay_lr_schedule_fn = optax.join_schedules(
            schedules=[warmup_fn, decay_fn],
            boundaries=[self.training_config.warmup_steps],
        )

        # We use Optax's "masking" functionality to not apply weight decay
        # to bias and LayerNorm scale parameters. decay_mask_fn returns a
        # mask boolean with the same structure as the parameters.
        # The mask is True for parameters that should be decayed.
        def decay_mask_fn(params):
            flat_params = traverse_util.flatten_dict(params)
            flat_mask = {
                path: (
                    path[-1] != "bias"  # type: ignore
                    and path[-2:]
                    not in [("layer_norm", "scale"), ("final_layer_norm", "scale")]
                )
                for path in flat_params
            }
            return traverse_util.unflatten_dict(flat_mask)

        # create adam optimizer
        if self.training_config.adafactor:
            # We use the default parameters here to initialize adafactor,
            # For more details about the parameters please check https://github.com/deepmind/optax/blob/ed02befef9bf81cbbf236be3d2b0e032e9ed4a40/optax/_src/alias.py#L74
            optimizer = optax.adafactor(
                learning_rate=linear_decay_lr_schedule_fn,
            )
        else:
            optimizer = optax.adamw(
                learning_rate=linear_decay_lr_schedule_fn,
                b1=self.training_config.adam_beta1,
                b2=self.training_config.adam_beta2,
                weight_decay=self.training_config.weight_decay,
                mask=decay_mask_fn,
            )

        # Setup train state
        state = train_state.TrainState.create(
            apply_fn=self.model.__call__,
            params=self.model.params,
            tx=optimizer,
        )

        # Define gradient update step fn
        def train_step(state, batch, dropout_rng):
            dropout_rng, new_dropout_rng = jax.random.split(dropout_rng)

            def loss_fn(params):
                labels = batch.pop("labels")

                logits = state.apply_fn(
                    **batch, params=params, dropout_rng=dropout_rng, train=True
                )[0]

                # compute loss
                loss = optax.softmax_cross_entropy(
                    logits, onehot(labels, logits.shape[-1])
                ).mean()

                return loss

            grad_fn = jax.value_and_grad(loss_fn)
            loss, grad = grad_fn(state.params)
            grad = jax.lax.pmean(grad, "batch")
            new_state = state.apply_gradients(grads=grad)

            metrics = jax.lax.pmean(
                {
                    "loss": loss,
                    "learning_rate": linear_decay_lr_schedule_fn(state.step),
                },
                axis_name="batch",
            )

            return new_state, metrics, new_dropout_rng

        # Create parallel version of the train step
        p_train_step = jax.pmap(train_step, "batch", donate_argnums=(0,))

        # Define eval fn
        def eval_step(params, batch):
            labels = batch.pop("labels")

            logits = self.model(**batch, params=params, train=False)[0]

            # compute loss
            loss = optax.softmax_cross_entropy(logits, onehot(labels, logits.shape[-1]))

            # compute accuracy
            accuracy = jnp.equal(jnp.argmax(logits, axis=-1), labels)

            # summarize metrics
            metrics = {"loss": loss.mean(), "accuracy": accuracy.mean()}
            metrics = jax.lax.pmean(metrics, axis_name="batch")

            return metrics

        p_eval_step = jax.pmap(eval_step, "batch", donate_argnums=(0,))

        # Replicate the train state on each device
        state = jax_utils.replicate(state)

        train_time = 0
        epochs = tqdm(range(num_epochs), desc=f"Epoch ... (1/{num_epochs})", position=0)
        for epoch in epochs:
            # ======================== Training ================================
            train_start = time.time()
            train_metrics = []

            # Create sampling rng
            rng, input_rng = jax.random.split(self.rng)

            # Generate an epoch by shuffling sampling indices from the train dataset
            num_train_samples = len(tokenized_datasets["train"])
            train_samples_idx = jax.random.permutation(
                input_rng, jnp.arange(num_train_samples)
            )
            train_batch_idx = generate_batch_splits(train_samples_idx, train_batch_size)

            # Gather the indexes for creating the batch and do a training step
            for step, batch_idx in enumerate(
                tqdm(train_batch_idx, desc="Training...", position=1)
            ):
                samples = [tokenized_datasets["train"][int(idx)] for idx in batch_idx]
                model_inputs = data_collator(samples)

                # Model forward
                model_inputs = shard(model_inputs.data)
                state, train_metric, dropout_rngs = p_train_step(
                    state, model_inputs, dropout_rngs
                )
                train_metrics.append(train_metric)

                cur_step = epoch * (num_train_samples // train_batch_size) + step

                if cur_step % self.training_config.logging_steps == 0 and cur_step > 0:
                    # Save metrics
                    train_metric = jax_utils.unreplicate(train_metric)
                    train_time += time.time() - train_start
                    if summary_writer is not None and jax.process_index() == 0:
                        write_train_metric(
                            summary_writer, train_metrics, train_time, cur_step
                        )

                    epochs.write(
                        f"Step... ({cur_step} | Loss: {train_metric['loss'].mean()}, Learning Rate: {train_metric['learning_rate'].mean()})"
                    )

                    train_metrics = []

                if cur_step % self.training_config.eval_steps == 0 and cur_step > 0:
                    # ======================== Evaluating ==============================
                    num_eval_samples = len(tokenized_datasets["validation"])
                    eval_samples_idx = jnp.arange(num_eval_samples)
                    eval_batch_idx = generate_batch_splits(
                        eval_samples_idx, eval_batch_size
                    )

                    eval_metrics = []
                    for i, batch_idx in enumerate(
                        tqdm(eval_batch_idx, desc="Evaluating ...", position=2)
                    ):
                        samples = [
                            tokenized_datasets["validation"][int(idx)]
                            for idx in batch_idx
                        ]
                        model_inputs = data_collator(samples)

                        # Model forward
                        model_inputs = shard(model_inputs.data)
                        metrics = p_eval_step(state.params, model_inputs)
                        eval_metrics.append(metrics)

                    # get eval metrics
                    eval_metrics = get_metrics(eval_metrics)
                    eval_metrics = jax.tree_map(jnp.mean, eval_metrics)

                    # Update progress bar
                    epochs.write(
                        f"Step... ({cur_step} | Loss: {eval_metrics['loss']}, Acc: {eval_metrics['accuracy']})"
                    )

                    # Save metrics
                    if summary_writer is not None and jax.process_index() == 0:
                        cur_step = epoch * (
                            len(tokenized_datasets["train"]) // train_batch_size
                        )
                        write_eval_metric(summary_writer, eval_metrics, cur_step)

                if cur_step % self.training_config.save_steps == 0 and cur_step > 0:
                    # save checkpoint after each epoch and push checkpoint to the hub
                    if jax.process_index() == 0:
                        params = jax.device_get(
                            jax.tree_map(lambda x: x[0], state.params)
                        )
                        self.model.save_pretrained(
                            self.training_config.output_dir,
                            params=params,
                            push_to_hub=self.training_config.push_to_hub,
                            commit_message=f"Saving weights and logs of step {cur_step}",
                        )

    def _check_output_dir_is_empty(self) -> None:
        if (
            os.path.exists(self.training_config.output_dir)
            and os.listdir(self.training_config.output_dir)
            and self.training_config.do_train
            and not self.training_config.overwrite_output_dir
        ):
            raise ValueError(
                f"Output directory ({self.training_config.output_dir}) already exists and is not empty."
                "Use --overwrite_output_dir to overcome."
            )

    def _get_logger(self) -> logging.Logger:
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
            level="NOTSET",
            datefmt="[%X]",
        )

        logger = logging.getLogger(__name__)
        return logger
