import logging


def configure_logging(caller: str):
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"log/{caller}.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
