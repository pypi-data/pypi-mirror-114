from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
import datasets
import jax
import jax.numpy as jnp
import numpy as np
from omegaconf import MISSING
import optax
import flax
from tqdm import tqdm
from flax import jax_utils, traverse_util
from flax.training import train_state
from flax.training.common_utils import get_metrics, onehot, shard
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
    PreTrainedTokenizerBase,
    AutoTokenizer,
)
from transformers.tokenization_utils_base import VERY_LARGE_INTEGER
from functools import partial
from flax import jax_utils, struct, traverse_util

from git_t5.data import compute_input_and_target_lengths, prepare_dataset

# pylint: disable=abstract-method
class TrainState(train_state.TrainState):
    loss_fn: Callable = struct.field(pytree_node=False)


@dataclass
class ModelConfig:
    model_path: Optional[str] = None
    model_type: Optional[str] = None
    config_name: Optional[str] = None
    tokenizer_path: Optional[str] = None
    cache_dir: Optional[str] = None
    use_fast_tokenizer: bool = True
    dtype: str = "float32"


@dataclass
class DataConfig:
    dataset_name: Optional[str] = None
    dataset_config_name: Optional[str] = None
    dataset_path: Optional[str] = None
    dataset_column: Optional[str] = None
    overwrite_cache: bool = False
    validation_size: float = 0.05
    max_sequence_length: Optional[int] = None
    num_workers: Optional[int] = None
    mlm_probability: float = 0.15
    mean_noise_span_length: float = 3.0


@dataclass
class TrainingConfig(TrainingArguments):
    output_dir: str = MISSING
    eval_steps: Optional[int] = None
    eval_strategy: IntervalStrategy = IntervalStrategy.NO
    lr_scheduler_type: SchedulerType = SchedulerType.LINEAR
    logging_strategy: IntervalStrategy = IntervalStrategy.STEPS
    save_strategy: IntervalStrategy = IntervalStrategy.STEPS
    push_to_hub_model_id: Optional[str] = None
    push_to_hub_organization: Optional[str] = None
    push_to_hub_token: Optional[str] = None


def tokenize_fn(
    tokenizer: PreTrainedTokenizerBase,
    column: str,
) -> Callable[..., Dict[str, Union[List[List[int]], np.ndarray]]]:
    def wrap_fn(
        examples: Dict[str, List[str]]
    ) -> Dict[str, Union[List[List[int]], np.ndarray]]:
        return tokenizer(examples[column], return_attention_mask=False)  # type: ignore

    return wrap_fn


class T5PreTrainingModule:
    dataset: datasets.DatasetDict
    tokenizer: PreTrainedTokenizerBase
    config: T5Config
    model: FlaxT5ForConditionalGeneration
    max_sequence_length: int
    input_length: int
    target_length: int

    def __init__(self, model_cfg: ModelConfig, data_cfg: DataConfig, seed: int) -> None:
        self.model_cfg = model_cfg
        self.data_cfg = data_cfg
        self.seed = seed

    def setup(self) -> None:
        self.tokenizer = self.load_tokenizer()
        self.config = self.load_config(len(self.tokenizer))  # type: ignore
        self.model = self.load_model(self.config)

        self.max_sequence_length = (
            self.data_cfg.max_sequence_length or VERY_LARGE_INTEGER
        )
        self.max_sequence_length = min(
            self.max_sequence_length, self.tokenizer.model_max_length
        )
        self.input_length, self.target_length = compute_input_and_target_lengths(
            self.max_sequence_length,
            noise_density=self.data_cfg.mlm_probability,
            mean_noise_span_length=self.data_cfg.mean_noise_span_length,
            extra_tokens_per_span_inputs=1,
            extra_tokens_per_span_targets=1,
        )

        self.dataset = self.load_dataset()
        self.dataset = self.prepare_dataset(self.dataset)

    @partial(jax.pmap, axis_name="batch")
    def train_step(
        self,
        state: TrainState,
        dropout_rng: jnp.ndarray,
        **model_inputs: Any,
    ) -> Tuple[TrainState, Dict[str, jnp.ndarray], jnp.ndarray]:
        def loss_fn(params):
            labels = model_inputs.pop("labels")
            outputs = state.apply_fn(
                **model_inputs,
                params=params,
                dropout_rng=dropout_rng,
                train=True,
            )

            # compute loss
            logits = outputs[0]
            labels = onehot(labels, logits.shape[-1])
            loss = optax.softmax_cross_entropy(logits, labels).mean()

            return loss

        dropout_rng, new_dropout_rng = jax.random.split(dropout_rng)

        grad_fn = jax.value_and_grad(loss_fn)
        loss, grads = grad_fn(state.params)
        grads = jax.lax.pmean(grads, "batch")
        state = state.apply_gradients(grads=grads)

        metrics = {
            "loss": loss,
            "learning_rate": linear_decay_lr_schedule_fn(state.step),  # TODO:
        }
        metrics = jax.lax.pmean(metrics, axis_name="batch")

        return state, metrics, new_dropout_rng

    @partial(jax.pmap, axis_name="batch")
    def valid_step(
        self,
        state: TrainState,
        **model_inputs: Any,
    ) -> Dict[str, jnp.ndarray]:
        labels = model_inputs.pop("labels")
        outputs = state.apply_fn(**model_inputs, params=state.params, train=False)

        # compute loss
        logits = outputs[0]
        labels = onehot(labels, logits.shape[-1])
        loss = optax.softmax_cross_entropy(logits, labels).mean()
        # compute accuracy
        accuracy = jnp.equal(jnp.argmax(logits, axis=-1), labels).mean()

        metrics = {"loss": loss, "accuracy": accuracy}
        metrics = jax.lax.pmean(metrics, axis_name="batch")

        return metrics

    def prepare_dataset(self, dataset: datasets.DatasetDict) -> datasets.DatasetDict:
        if self.data_cfg.dataset_column is None:
            raise ValueError(
                "You must provide a `dataset_column` to specify which column of the dataset to use."
            )

        dataset = prepare_dataset(
            dataset,
            tokenize_fn(self.tokenizer, self.data_cfg.dataset_column),
            input_length=self.input_length,
            batch_size=128,
            load_from_cache_file=not self.data_cfg.overwrite_cache,
            num_workers=self.data_cfg.num_workers,
        )

        return dataset

    def load_dataset(self) -> datasets.DatasetDict:
        if self.data_cfg.dataset_name is not None:
            dataset = datasets.load_dataset(
                self.data_cfg.dataset_name,
                self.data_cfg.dataset_config_name,
                cache_dir=self.model_cfg.cache_dir,
            )

            if not isinstance(dataset, datasets.DatasetDict):
                dataset = datasets.DatasetDict(train=dataset)

            if "validation" not in dataset.keys():
                valid_percentage = int(self.data_cfg.validation_size * 100)
                dataset["validation"] = datasets.load_dataset(
                    self.data_cfg.dataset_name,
                    self.data_cfg.dataset_config_name,
                    split=f"train[:{valid_percentage}%]",
                    cache_dir=self.model_cfg.cache_dir,
                )
                dataset["train"] = datasets.load_dataset(
                    self.data_cfg.dataset_name,
                    self.data_cfg.dataset_config_name,
                    split=f"train[{valid_percentage}%:]",
                    cache_dir=self.model_cfg.cache_dir,
                )
        elif self.data_cfg.dataset_path is not None:
            dataset = datasets.load_from_disk(self.data_cfg.dataset_path)
            if not isinstance(dataset, datasets.DatasetDict):
                dataset = datasets.DatasetDict(train=dataset)

            if "validation" not in dataset.keys():
                dataset = dataset["train"].train_test_split(
                    test_size=self.data_cfg.validation_size,
                    load_from_cache_file=not self.data_cfg.overwrite_cache,
                )
                dataset["validation"] = dataset.pop("test")
        else:
            raise ValueError("`dataset_name` or `dataset_path` must be specified.")

        return dataset

    def load_tokenizer(self) -> PreTrainedTokenizerBase:
        if self.model_cfg.tokenizer_path is not None:
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_cfg.tokenizer_path,
                cache_dir=self.model_cfg.cache_dir,
                use_fast=self.model_cfg.use_fast_tokenizer,
            )
        elif self.model_cfg.model_path is not None:
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_cfg.model_path,
                cache_dir=self.model_cfg.cache_dir,
                use_fast=self.model_cfg.use_fast_tokenizer,
            )
        else:
            raise ValueError(
                "You are instantiating a new tokenizer from scratch. This is not supported by this script."
                "You can do it from another script, save it, and load it from here, using `tokenizer_path`."
            )

        assert isinstance(tokenizer, PreTrainedTokenizerBase)
        return tokenizer

    def load_config(self, vocab_size: int) -> T5Config:
        if self.model_cfg.config_name is not None:
            config = T5Config.from_pretrained(
                self.model_cfg.config_name,
                cache_dir=self.model_cfg.cache_dir,
                vocab_size=vocab_size,
            )
        elif self.model_cfg.model_path is not None:
            config = T5Config.from_pretrained(
                self.model_cfg.model_path,
                cache_dir=self.model_cfg.cache_dir,
                vocab_size=vocab_size,
            )
        else:
            config = CONFIG_MAPPING[self.model_cfg.model_type]()  # type: ignore
            # TODO: add logger warning

        assert isinstance(config, T5Config)
        return config

    def load_model(self, config: T5Config) -> FlaxT5ForConditionalGeneration:
        if self.model_cfg.model_path is not None:
            model = FlaxT5ForConditionalGeneration.from_pretrained(
                self.model_cfg.model_path,
                config=config,
                seed=self.seed,
                dtype=getattr(jnp, self.model_cfg.dtype),
            )
        else:
            model = FlaxT5ForConditionalGeneration(
                config,
                seed=self.seed,
                dtype=getattr(jnp, self.model_cfg.dtype),
            )

        return model
