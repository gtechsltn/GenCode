import os
from dataclasses import dataclass, field

import logging
from classes.GCodePreprocessing_Utils import GCodePreprocessingUtils
from log_config import configure_logging


@dataclass(frozen=True)
class DataCleaner:
    """

    A data class that computes what data to be cleaned and provides metrics before cleaning the data with the help of the helper classes

    Holds the information pertaining to the data before the source cleanup.

    Informations are stored in `log/cleanData.log`

    @author: Raja Thiurmal

    """

    cleanDataIn: str
    _preProcessor: GCodePreprocessingUtils
    _pwd: str = field(default=os.getcwd(), init=False,repr=False)
    _pre_clean_metric: tuple = field(init=False)
    py_files: list = field(init=False,repr=False)

    def __post_init__(self) -> None:
        # Enable looging to this file
        configure_logging()
        # Create a GCodePreprocessingUtils instance
        self._preProcessor: GCodePreprocessingUtils = GCodePreprocessingUtils(self.cleanDataIn)
        logging.info(f"Currently working on: {self._pwd}")
        # Compute the metrics
        self._pre_clean_metric, files_abspath = self._preProcessor.scan_files(
            scanFilesUnder=self._preProcessor.sourcefolder
        )
        logging.info(
            f"""Files under {self._preProcessor.sourcefolder} is of
                        {self._pre_clean_metric[0]:.2f} KB
                        {self._pre_clean_metric[1]:.2f} MB
                        {self._pre_clean_metric[2]:.2f} GB
                    """
        )
        logging.info(
            f"{len(files_abspath)} files in the '{self._preProcessor.sourcefolder}'"
        )
        # Hold back only the py files
        self.py_files = list(filter(lambda file: file.endswith(".py"), files_abspath))

        logging.info(
            f"{len(self.py_files)} python files in the '{self._preProcessor.sourcefolder}'"
        )
        logging.info(
            f"{(len(self.py_files)/len(files_abspath))*100:.3f} % of downloaded data is usable."
        )


def main() -> None:
    folder_path = "download"
    p = DataCleaner(cleanDataIn=folder_path)
    print(p)


if __name__ == "__main__":
    main()
# for root, dirs, files in tqdm(os.walk(folder_path)):
#     # Remove non .py files
#     for file in files:
#         full_path = os.path.join(root, file)
#         # Ignoring .py files
#         if full_path.endswith(".py"):
#             logging.info(f"retaining (.py file) {full_path}")
#             pass
#             # print(full_path)
#         else:
#             # print(f">>> Deleting >>> {full_path} ")
#             # Set all permissions before deleting
#             logging.info(f"Force deleting: {full_path}")
#             os.chmod(full_path, 0o777)
#             os.remove(full_path)

print("Completed... 🧹")
logging.info("Completed 🧹")
