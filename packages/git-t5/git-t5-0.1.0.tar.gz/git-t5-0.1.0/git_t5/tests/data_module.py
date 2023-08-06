import datasets
import time
from git_t5.core.model_trainer import DataConfig, ModelConfig, T5PreTrainingModule

model_cfg = ModelConfig(
    model_type="t5",
    config_name="t5-base",
    tokenizer_path="/Users/mozharovsky/Desktop/git-t5-tokenizer/tokenizer",
    cache_dir="/Users/mozharovsky/Desktop/git-t5-tokenizer/model",
)

data_cfg = DataConfig(
    dataset_path="/Users/mozharovsky/Desktop/git-t5-tokenizer/data",
    dataset_column="text",
    max_sequence_length=512,
    overwrite_cache=True,
    num_workers=8,
)

module = T5PreTrainingModule(model_cfg, data_cfg, seed=1)

t1 = time.time()
module.setup()
t2 = time.time()

print(f"Elapsed time: {t2-t1} sec")

print(module.dataset)

# def tokenize_fn(examples):
#     return module.tokenizer(examples["text"], return_attention_mask=False)  # type: ignore


# dataset = module.load_dataset().map(
#     tokenize_fn,
#     # batched=False,
#     # remove_columns=column_names(dataset),
#     # load_from_cache_file=not self.data_cfg.overwrite_cache,
#     num_proc=2,
# )
# dataset = module.load_dataset()
# tokenizer = module.load_tokenizer()
