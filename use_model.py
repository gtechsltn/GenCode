import time
import logging
from log_config import configure_logging
from tokenizers import ByteLevelBPETokenizer

from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
)


configure_logging()


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

text = "Hello programmer have a good day!"

logging.debug(f"Encoding: {text}")

encoded = tokenizer.encode(text)

logging.debug(f"Encoded result: {encoded}")
logging.debug(f"Decoded result: {tokenizer.decode(encoded)}")
try:
    assert tokenizer.decode(encoded) == text
except:
    logging.error(f"assertinon failed: {tokenizer.decode(encoded) == text}")

model = GPT2LMHeadModel.from_pretrained("GCodeModel/checkpoint-400") # add your checkpooint file path

print("Type 'q' or 'quit' to exit this terminal")
while True:
    imp = input("✨>>> ")
    if imp == 'q' or imp == 'quit':
        exit()
    logging.debug(f"User prompt: {imp}")
    input_ids = tokenizer.encode(imp, return_tensors="pt")
    logging.debug(f"Prompt tensor: {input_ids}")
    beam_output = model.generate(
        inputs=input_ids,
        max_length=512,
        num_beams=10,
        temperature=0.7,
        no_repeat_ngram_size=5,
    )
    logging.debug(f"Beam output: {beam_output}")

    for beam in beam_output:
        out = tokenizer.decode(beam)
        logging.debug(f"Generated output: {out}")
        beam = out.replace("<N>", "\n")
        print(str(beam),flush=True)
        
