import logging


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="logfile.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
