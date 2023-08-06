from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

import datasets
import numpy as np
from git_t5.data import (
    DataCollatorForT5MLM,
    DataLoader,
    compute_input_and_target_lengths,
    prepare_dataset,
)
from transformers import AutoTokenizer, PreTrainedTokenizerBase
from transformers.tokenization_utils_base import VERY_LARGE_INTEGER
from omegaconf import MISSING

if TYPE_CHECKING:
    from .trainer import T5Trainer
else:
    T5Trainer = Any


def tokenize_fn(
    tokenizer: PreTrainedTokenizerBase,
    column: str,
) -> Callable[..., Dict[str, Union[List[List[int]], np.ndarray]]]:
    def wrap_fn(
        examples: Dict[str, List[str]]
    ) -> Dict[str, Union[List[List[int]], np.ndarray]]:
        return tokenizer(examples[column], return_attention_mask=False)  # type: ignore

    return wrap_fn


@dataclass
class DataModuleConfig:
    pass


@dataclass
class T5DataModuleConfig(DataModuleConfig):
    dataset_name: Optional[str] = None
    dataset_config_name: Optional[str] = None
    dataset_path: Optional[str] = None
    dataset_column: Optional[str] = None
    model_path: Optional[str] = MISSING  # derive from model config
    tokenizer_path: Optional[str] = MISSING  # derive from model config
    use_fast_tokenizer: bool = MISSING  # derive from model config
    cache_dir: Optional[str] = MISSING  # derive from model config
    overwrite_cache: bool = False
    validation_size: float = 0.05
    max_sequence_length: Optional[int] = None
    train_batch_size: int = 8
    eval_batch_size: int = 8
    num_workers: Optional[int] = None
    mlm_probability: float = 0.15
    mean_noise_span_length: float = 3.0
    decoder_start_token_id: int = MISSING
    seed: int = MISSING  # derive from model config


class T5DataModule:
    dataset: datasets.DatasetDict
    tokenizer: PreTrainedTokenizerBase
    data_collator: DataCollatorForT5MLM
    max_sequence_length: int
    input_length: int
    target_length: int
    trainer: Optional[T5Trainer] = None

    def __init__(self, config: T5DataModuleConfig) -> None:
        self.config = config

    def setup(self) -> None:
        self.tokenizer = self.load_tokenizer()

        self.max_sequence_length = self.config.max_sequence_length or VERY_LARGE_INTEGER
        self.max_sequence_length = min(
            self.max_sequence_length, self.tokenizer.model_max_length
        )
        self.input_length, self.target_length = compute_input_and_target_lengths(
            self.max_sequence_length,
            noise_density=self.config.mlm_probability,
            mean_noise_span_length=self.config.mean_noise_span_length,
            extra_tokens_per_span_inputs=1,
            extra_tokens_per_span_targets=1,
        )

        eos_token_id = self.tokenizer.eos_token_id
        pad_token_id = self.tokenizer.pad_token_id
        sentinel_token_id = self.tokenizer.convert_tokens_to_ids("<extra_id_0>")  # type: ignore
        if eos_token_id is None:
            raise ValueError("Tokenizer must have an existing `eos_token_id` value.")
        if pad_token_id is None:
            raise ValueError("Tokenizer must have an existing `pad_token_id` value.")
        if sentinel_token_id is None:
            raise ValueError("Tokenizer must have an existing `eos_token_id` value.")

        self.data_collator = DataCollatorForT5MLM(
            tokenizer=self.tokenizer,
            noise_density=self.config.mlm_probability,
            mean_noise_span_length=self.config.mean_noise_span_length,
            input_length=self.max_sequence_length,
            target_length=self.target_length,
            eos_token_id=eos_token_id,
            pad_token_id=pad_token_id,
            sentinel_token_id=sentinel_token_id,
            decoder_start_token_id=self.config.decoder_start_token_id,
        )

        self.dataset = self.load_dataset()
        self.dataset = self.prepare_dataset(self.dataset)

    def train_dataloader(self) -> DataLoader:
        return DataLoader(
            self.dataset["train"],
            batch_size=self.config.train_batch_size,
            collate_fn=self.data_collator,
            shuffle=True,
            seed=self.config.seed,
        )

    def valid_dataloader(self) -> DataLoader:
        return DataLoader(
            self.dataset["validation"],
            batch_size=self.config.eval_batch_size,
            collate_fn=self.data_collator,
            shuffle=False,
            seed=None,
        )

    def prepare_dataset(self, dataset: datasets.DatasetDict) -> datasets.DatasetDict:
        if self.config.dataset_column is None:
            raise ValueError(
                "You must provide a `dataset_column` to specify which column of the dataset to use."
            )

        dataset = prepare_dataset(
            dataset,
            tokenize_fn(self.tokenizer, self.config.dataset_column),
            input_length=self.input_length,
            batch_size=128,
            load_from_cache_file=not self.config.overwrite_cache,
            num_workers=self.config.num_workers,
        )

        return dataset

    def load_dataset(self) -> datasets.DatasetDict:
        if self.config.dataset_name is not None:
            dataset = datasets.load_dataset(
                self.config.dataset_name,
                self.config.dataset_config_name,
                cache_dir=self.config.cache_dir,
            )

            if not isinstance(dataset, datasets.DatasetDict):
                dataset = datasets.DatasetDict(train=dataset)

            if "validation" not in dataset.keys():
                valid_percentage = int(self.config.validation_size * 100)
                dataset["validation"] = datasets.load_dataset(
                    self.config.dataset_name,
                    self.config.dataset_config_name,
                    split=f"train[:{valid_percentage}%]",
                    cache_dir=self.config.cache_dir,
                )
                dataset["train"] = datasets.load_dataset(
                    self.config.dataset_name,
                    self.config.dataset_config_name,
                    split=f"train[{valid_percentage}%:]",
                    cache_dir=self.config.cache_dir,
                )
        elif self.config.dataset_path is not None:
            dataset = datasets.load_from_disk(self.config.dataset_path)
            if not isinstance(dataset, datasets.DatasetDict):
                dataset = datasets.DatasetDict(train=dataset)

            if "validation" not in dataset.keys():
                dataset = dataset["train"].train_test_split(
                    test_size=self.config.validation_size,
                    load_from_cache_file=not self.config.overwrite_cache,
                )
                dataset["validation"] = dataset.pop("test")
        else:
            raise ValueError("`dataset_name` or `dataset_path` must be specified.")

        return dataset

    def load_tokenizer(self) -> PreTrainedTokenizerBase:
        if self.config.tokenizer_path is not None:
            tokenizer = AutoTokenizer.from_pretrained(
                self.config.tokenizer_path,
                cache_dir=self.config.cache_dir,
                use_fast=self.config.use_fast_tokenizer,
            )
        elif self.config.model_path is not None:
            tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_path,
                cache_dir=self.config.cache_dir,
                use_fast=self.config.use_fast_tokenizer,
            )
        else:
            raise ValueError(
                "You are instantiating a new tokenizer from scratch. This is not supported by this script. "
                "You can do it from another script, save it, and load it from here, using `tokenizer_path`."
            )

        assert isinstance(tokenizer, PreTrainedTokenizerBase)
        return tokenizer
