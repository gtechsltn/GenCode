import os
import logging
from dataclasses import dataclass, field
from typing import Union
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


@dataclass
class MakeModel:
    paths: list[str] = field(init=False, repr=True)
    tokenizer: ByteLevelBPETokenizer = field(init=False, repr=True)

    def __post_init__(self) -> None:
        configure_logging()
        # self.paths = os.listdir("data")
        self.paths = [os.path.join('./data/', f) for f in os.listdir("data")]
        logging.info(f"Dataset used are {self.paths}")
        self.paths = [os.path.join(os.getcwd(), path) for path in self.paths]

    def __precheck_folders(self) -> None:
        """
        Actions realated to the token folder availability
        """
        # token_dir = os.path.dirname('./token')
        token_dir = "./token"
        if os.path.exists(token_dir):
            logging.warning(f"Tokens directory already available.")
            logging.error(
                f"Please clear or remove the tokens directory and run this script again"
            )
            raise Exception("Please remove the token folder")
            
        else:
            logging.info(f"No directory for tokens, creating one for you 🫶🏻")
            os.makedirs(token_dir)

    def __createTokens(self):
        """
        This function creates the tokens with the available dataset (i.e) the files under the data directory.

        Makes use of the ByteLevelBPETokenizer to create the tokens

        `Vocab size` : 1024

        `Minimum frequency` : 2
        """

        logging.info(f"Started tokenising ...")

        self.tokenizer = ByteLevelBPETokenizer()
        self.tokenizer.train(
            files=self.paths,
            vocab_size=1024,
            min_frequency=2,
            special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"],
        )

        self.tokenizer.save_model("./token/")
        logging.info(f"Tokens created")
        logging.info(f"Created vocabs.json and merges.txt in token/")

        


    def _testTokens(self, tokenizer) -> None:
        logging.debug(
            "---------------------------------------------------------------------"
        )
        logging.debug(
            f"Testing the model if it is able to decode and encode the given text"
        )
        text = "Hello programmer have a good day!"

        logging.debug(f"Encoding: {text}")

        encoded = tokenizer.encode(text)

        logging.debug(f"Encoded result: {encoded}")
        logging.debug(f"Decoded result: {tokenizer.decode(encoded)}")
        logging.debug(
            "---------------------------------------------------------------------"
        )

    def useModel(self, token_dir: Union[str, None] = "token") -> None:
        """
        Make use of the tokens available:

        If you have already created your own tokes with someother supporing tokeniser,

        Please pass the directory information where the tokens and merges.txt files are placed

        By default the `token_dir` = "token"
        """
        logging.info(
            f"Making use of available vocabs.json and merges.txt in {token_dir}"
        )
        self.tokenizer = GPT2Tokenizer.from_pretrained(token_dir)
        self.tokenizer.add_special_tokens(
            {
                "eos_token": "</s>",
                "bos_token": "</s>",
                "unk_token": "</unk>",
                "pad_token": "<pad>",
                "mask_token": "<mask>",
            }
        )
        self._testTokens(tokenizer=self.tokenizer)
        logging.info(f"Completed the preprocessing steps. 😎")

    def __makeTrainer(self) -> Trainer:
        """
        Makes use of the vocabs available in the token directory
        """
        config = GPT2Config(
            vocab_size=self.tokenizer.vocab_size,
            bos_token=self.tokenizer.bos_token_id,
            eos_token=self.tokenizer.eos_token_id,
        )

        # Train the model

        model = GPT2LMHeadModel(config=config)

        # load dataset with lazy loading
        dataset = load_dataset("text", data_files=self.paths)

        def encode(lines):
            return self.tokenizer(
                lines["text"],
                add_special_tokens=True,
                padding=True,         # Add padding to make all sequences the same length
                truncation=True,      # Truncate sequences longer than max_length
                max_length=512,
            )

        dataset.set_transform(encode)

        dataset = dataset["train"]

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer, mlm=True, mlm_probability=0.15
        )

        training_args = TrainingArguments(
            output_dir="GCodeModel",
            overwrite_output_dir=True,
            num_train_epochs=1,
            per_device_eval_batch_size=10, # Reduce this number if you have low resource to work with
            fp16=True, # use half-precision floating-point numbers, which reduces memory usage and speeds up training
            save_steps=50,  # Saves the model evey 50 steps
            save_total_limit=2, # Have only last 2 steps / Purge older steps
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
        return trainer

    def startModelCreation(self) -> Trainer:
        # Cheack for the folder avalability
        self.__precheck_folders()
        # Create the tokens
        self.__createTokens()
        # Make use of the thus created model
        self.useModel()
        # Train the model
        return self.__makeTrainer()


def main():
    mm = MakeModel()
    trainer = mm.startModelCreation()
    trainer.train()
    print("Model is created under /GCodeModel")
    print("You are good to run use_model.py")


if __name__ == "__main__":
    main()

