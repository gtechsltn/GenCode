import os
import logging
from log_config import configure_logging
from tokenizers import ByteLevelBPETokenizer

from transformers import (
    GPT2Config,
    GPT2LMHeadModel,
    GPT2Tokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)
from datasets import load_dataset


configure_logging()

# Create vocabs
paths = ["./data/GCodeT.txt"]

logging.info(f"Dataset used are {paths}")

token_dir = os.path.dirname('./token/"')
if not os.path.exists(token_dir):
    logging.info(f"No vocabs found. Creating vocabs for {paths}")
    os.makedirs(token_dir)

    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(
        files=paths,
        vocab_size=1024,
        min_frequency=2,
        special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"],
    )

    tokenizer.save_model("./token/")

    logging.info(f"Created vocabs.json and merges.txt in token/")

# Make use of the vocabs
logging.info(f"Making use of available vocabs.json and merges.txt")

tokenizer = GPT2Tokenizer.from_pretrained("token")
tokenizer.add_special_tokens(
    {
        "eos_token": "</s>",
        "bos_token": "</s>",
        "unk_token": "</unk>",
        "pad_token": "<pad>",
        "mask_token": "<mask>",
    }
)
logging.info(f"Completed the preprocessing steps. 😎")

text = "Hello programmer have a good day!"

logging.debug(f"Encoding: {text}")

encoded = tokenizer.encode(text)

logging.debug(f"Encoded result: {encoded}")
logging.debug(f"Decoded result: {tokenizer.decode(encoded)}")

# Config
pwd = os.getcwd()
config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    bos_token=tokenizer.bos_token_id,
    eos_token=tokenizer.eos_token_id,
)

# Train the model

model = GPT2LMHeadModel(config=config)

# load dataset with lazy loading
dataset = load_dataset("text", data_files=paths)


def encode(lines):
    return tokenizer(
        lines["text"],
        add_special_tokens=True,
        #truncate=True,
        max_length=512,
    )


dataset.set_transform(encode)

dataset = dataset["train"]

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)


training_args = TrainingArguments(
    output_dir="GCodeModel",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_eval_batch_size=10,
    # per_gpu_train_batch_size=64,
    save_steps=100,  # Saves the model evey 100 steps
    save_total_limit=2,
    prediction_loss_only=True,
    remove_unused_columns=False,
    use_mps_device=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)


trainer.train()


trainer.save_model("GCodeModel")
