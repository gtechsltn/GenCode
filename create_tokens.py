import os
import logging
from log_config import configure_logging
from tokenizers import ByteLevelBPETokenizer

from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer

configure_logging()

# Create vocabs
paths = ["./data/GCodeT.txt"]

logging.info(f'Dataset used are {paths}')

make_dataset_ReadError = os.path.dirname('./token/"')
if not os.path.exists(make_dataset_ReadError):
    logging.info(f"No vocabs found. Creating vocabs for {paths}")
    os.makedirs(make_dataset_ReadError)

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

text='Hello programmer have a good day!'
logging.debug(f"Encoding: {text}")
encoded = tokenizer.encode(text)
logging.debug(f"Encoded result: {encoded}")
logging.debug(f"Decoded result: {tokenizer.decode(encoded)}")