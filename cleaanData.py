import os
from dataclasses import dataclass, field

import logging
from classes.CleanBatch import Batch
from classes.GCodePreprocessing_Utils import GCodePreprocessingUtils
from log_config import configure_logging
from make_dataset import MakeDataset


@dataclass(frozen=False)
class DataCleaner():
    """

    A data class that computes what data to be cleaned and provides metrics before cleaning the data with the help of the helper classes

    Holds the information pertaining to the data before the source cleanup.

    Informations are stored in `log/cleanData.log`

    @author: Raja Thiurmal

    """

    cleanDataIn: str
    _preProcessor: GCodePreprocessingUtils = field(init=False, repr=False)
    _makeDataset: MakeDataset = field(init=False, repr=False)
    _pwd: str = field(default=os.getcwd(), init=False, repr=False)
    batch_list: list[Batch] = field(default_factory= list[Batch],init=False,repr=False)
    py_files: list = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # Enable looging to this file
        configure_logging()
        # Create a GCodePreprocessingUtils instance
        self._preProcessor = GCodePreprocessingUtils(self.cleanDataIn)
        self._makeDataset = MakeDataset()
        logging.info(f"Currently working on: {self._pwd}")
        logging.info(self)

    def start_batch_process(self) -> None:
        logging.info('Starting Batch process')
        percentage = 0.10
        total_folder_count = len(os.listdir(self.cleanDataIn))
        folder_start_segment = 0
        folder_end_segment = int(total_folder_count * percentage)
        batch_size = folder_end_segment - folder_start_segment
        batch_number = 0
        f_count = 0
        logging.info(f"Total folders to scann: {total_folder_count}")
        logging.info(f"Each batch size: {batch_size}")

        while f_count < total_folder_count:
            print(f"Batch {batch_number}/{(total_folder_count//batch_size)} ")
            if total_folder_count - f_count < batch_size:
                folders_to_check = os.listdir(self.cleanDataIn)[folder_start_segment:]
                f_count += total_folder_count - f_count
            else:
                folders_to_check = os.listdir(self.cleanDataIn)[
                    folder_start_segment:folder_end_segment
                ]
                f_count += batch_size
            
            # batch_number=batch_number,
            batch_metrics=self._preProcessor.folder_metrics(folder_list=folders_to_check, batch_number=batch_number)
            b = Batch(batch_number=batch_number,batch_metrics=batch_metrics, batch_folder_count=len(folders_to_check))
            self.batch_list.append(b)

            

            folder_start_segment = folder_end_segment
            folder_end_segment += batch_size
            # Log size info for each batch
            self._logBatchInfo(batch=b)
            # Create a dataset file for the batch
            py_file = [key for key in batch_metrics.keys() if key.endswith('.py')]
            self._makeDataset.create_dataset(file_list=py_file,batch=batch_number)

            batch_number += 1

    def _logBatchInfo(self,batch:Batch):
        batch_kb , batch_mb, batch_gb = 0,0,0
        for kb,mb,gb in list(batch.batch_metrics.values()):
            batch_kb+=kb
            batch_mb +=mb
            batch_gb +=gb 
        logging.info(
        f"""Batch {batch.batch_number}, Folders scannned {batch.batch_folder_count}:
            {batch_kb:.2f} KB
            {batch_mb:.2f} MB
            {batch_gb:.2f} GB
        """
        )

def main() -> None:
    folder_path = "download"
    #folder_path = "/Volumes/Untitled/May2023"
    dc = DataCleaner(cleanDataIn=folder_path)
    dc.start_batch_process()



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
