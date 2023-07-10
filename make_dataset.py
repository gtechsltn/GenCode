from dataclasses import dataclass, field
from io import TextIOWrapper
import os
from tqdm import tqdm

import logging
from classes.GCodeModel_Utils import GCodeModelUtils
from classes.GCodePreprocessing_Utils import GCodePreprocessingUtils
from log_config import configure_logging


@dataclass
class MakeDataset:
    # Configure logging
    configure_logging()

    file_list: list = field(default_factory=list, init=False)
    size_in_bytes: int = field(default=0, init=False)
    MAX_CHAR_LENGTH: int = field(default=512, init=False)  # Maximum context length
    MIN_CHAR_LENGTH: int = field(default=400, init=False)  # Minimum context length
    NEW_LINE: str = field(default="<N>", init=False)

    def __post_init__(self):
        configure_logging()
        self._precheck()

    def _precheck(self) -> None:
        # Create the data directory if it does not exist
        GC_folders = os.path.dirname("data/")
        if not os.path.exists(GC_folders):
            logging.info(f"Creating a folder for dataset")
            os.makedirs(GC_folders)
        else:
            logging.info(
                f"Folder for dataset already available. Contents may be apended"
            )

        # Create the error directory if it does not exist
        GC_folders = os.path.dirname("error/")
        if not os.path.exists(GC_folders):
            logging.info(f"Creating a folder for error")
            os.makedirs(GC_folders)
        else:
            logging.info(f"Folder for error already available. Contents may be apended")

    def create_dataset(self, file_list: list, batch: int) -> None:
        dataset_file = f"data/GCodeT_June_{batch}.txt"

        try:
            # Creating dataset file
            with open(dataset_file, "a", encoding="utf-8") as datasetFile:
                for pyFile in tqdm(
                    file_list, desc=f"Creating dataset for batch {batch}"
                ):
                    try:
                        pyContent = open(pyFile, "r", encoding="utf-8").read()
                    except Exception as e:
                        logging.error(
                            f"Error while reading {pyFile} for the bacth {batch}"
                        )
                        with open(
                            "error/read_error.log", "a", encoding="utf-8"
                        ) as w_error_file:
                            w_error_file.write(
                                f"Error while reading {pyFile} for the bacth {batch}\n"
                            )
                            w_error_file.write(f"{str(e)}\n")
                        logging.error(f"Refer to error/write_error.log")

                    try:
                        self._format_content(_content=pyContent, _fileObj=datasetFile)
                    except Exception as e:
                        logging.error(
                            f"Error while writing dataset with content from {pyFile} for the bacth {batch}"
                        )
                        with open(
                            "error/write_error.log", "a", encoding="utf-8"
                        ) as w_error_file:
                            w_error_file.write(
                                f"Error while creating dataset for the bacth {batch}\n"
                            )
                            w_error_file.write(str(e)+'\n')
                        logging.error(f"Refer to error/write_error.log")
        except Exception as e:
            logging.error(f"Error while creating dataset file {dataset_file}")
            logging.error(f"Refer to error/create_dataset_error.log")
            with open(
                "error/create_dataset_error.log", "a", encoding="utf-8"
            ) as c_error_file:
                c_error_file.write(f"Error while creating dataset file {dataset_file}\n")
                c_error_file.write(str(e)+'\n')
        finally:
            # When dataset creation is completed check for any errors
            if len(os.listdir("error")) == 0:
                logging.info(f"Dataset created 🥳")
            else:
                logging.error(f"Problem with creation of the dataset file 😿")
                logging.error(f"Check error directory for more info 🙁")

    def _format_content(self, _content: str, _fileObj: TextIOWrapper) -> str:
        # Replace new line with NEW_LINE
        formated_data = _content.replace("\n", self.NEW_LINE)
        if 100 < len(_content) <= self.MAX_CHAR_LENGTH:
            _fileObj.write(formated_data + "\n")
        else:
            sd = formated_data.split(f"{self.NEW_LINE}{self.NEW_LINE}")
            substring = ""
            for splite in sd:
                substring += splite + f"{self.NEW_LINE}{self.NEW_LINE}"
                if self.MIN_CHAR_LENGTH <= len(substring) <= self.MAX_CHAR_LENGTH:
                    _fileObj.write(substring + "\n")
                


'''

    logging.debug(f"Scanning files under {folder_path} ...")
    GUtils = GCodePreprocessingUtils(source=folder_path)
    (kb, mb, gb), file_list = GUtils.scan_files()
    logging.info(
        f"""Files under {folder_path} is of
                    {kb:.2f} KB
                    {mb:.2f} MB
                    {gb:.2f} GB
                """
    )
    # print(f"Scanned {len(file_list)} items")
    logging.debug(f"Scanned {len(file_list)} items")

    # Create the directory if it does not exist
    GCodeT = os.path.dirname("data/GCodeT.txt")
    if not os.path.exists(GCodeT):
        os.makedirs(GCodeT)

    file_counter = 0
    GCodeTFile = f"data/GCodeT_May2023_{file_counter}.txt"
    with open(GCodeTFile, "a", encoding="utf-8") as datasetFile:
        # Read each file, try to make the data fall in bounds with MAX_CHAR_LENGTH and MIN_CHAR_LENGTH
        try:
            for file in tqdm(file_list):
                # Check if the file has exceeded the read count
                if file_counter % 5 == 0:
                    datasetFile.close()
                    GCodeTFile = f"data/GCodeT_May2023_{file_counter}.txt"
                    # Create a new dataset file
                    datasetFile = open(GCodeTFile, "a", encoding="utf-8")

                try:
                    py_file_data = open(file, "r", encoding="utf-8").read()
                except Exception as ex:
                    logging.error(
                        f"Read error {file}. Refer to make_dataset_ReadError.txt for more inormation"
                    )
                    make_dataset_ReadError = os.path.dirname(
                        'error/make_dataset_ReadError.txt"'
                    )

                    if not os.path.exists(make_dataset_ReadError):
                        os.makedirs(make_dataset_ReadError)
                    with open(
                        "error/make_dataset_ReadError.txt", "a"
                    ) as make_dataset_ReadError:
                        make_dataset_ReadError.write(f"{file}\n{str(ex)}")
                        make_dataset_ReadError.write(str(ex) + "\n")
                    continue

                formated_data = py_file_data.replace("\n", NEW_LINE)
                if 100 < len(py_file_data) <= MAX_CHAR_LENGTH:
                    datasetFile.write(formated_data + "\n")

                    # break
                # Removes the extra white spaces
                else:
                    sd = formated_data.split(f"{NEW_LINE}{NEW_LINE}")
                    substring = ""
                    for splite in sd:
                        substring += splite + f"{NEW_LINE}{NEW_LINE}"
                        if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:
                            datasetFile.write(substring + "\n")

                        # print(substring)
                        # break
                logging.debug(f"Processing: {file}")
                logging.debug(f"Written to: {GCodeTFile}")
                file_counter += 1
        except Exception as e:
            logging.error(
                f"Error while processing:\n{GCodeTFile}. Refer to GCodeT_WriteError.txt for more information"
            )

            GCodeT_WriteError = os.path.dirname("error/GCodeT_WriteError.txt")
            if not os.path.exists(GCodeT_WriteError):
                os.makedirs(GCodeT_WriteError)
            with open("error/GCodeT_WriteError.txt", "a") as GCodeT_WriteError:
                GCodeT_WriteError.write(f"Error while processing:\n")
                GCodeT_WriteError.write(f"{str(e)}")

            # print(file)
            # print(str(e))
        finally:
            if len(os.listdir("error")) == 0:
                traning_sample_count, _, _ = GCodeModelUtils.model_params(batchSize=60)
                logging.info(f"Dataset with {traning_sample_count} vocabs created")
                logging.info(f"Dataset created 🥳")
                print(f"Dataset created 🥳. Good to create tokens with the vocabs")
            else:
                logging.info(f"Check error dorectory for more info 🙁")
'''
