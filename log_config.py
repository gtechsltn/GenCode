import logging
import os

def configure_logging():

    log_file_path = os.path.abspath(__file__)
    log_file_name : str = os.path.splitext(os.path.basename(log_file_path))[0]

    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"log/{log_file_name}.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
