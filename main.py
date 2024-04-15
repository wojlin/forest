import logging
import colorlog
import time

from forest_data import ForestData
from utils import Fetcher
from web import web

def setup_logging():
    logging.basicConfig(filename='forest.log', level=logging.DEBUG)
    logger = logging.getLogger("forest")
    # Create a colorlog formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
    )

    # Create console handler and set level to DEBUG
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add console handler to the logger
    logger.addHandler(console_handler)


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger("forest")

    logger.info(f"loading forest data...")
    start_time = time.time()
    forest = ForestData()
    end_time = time.time()
    logger.info(f"loading forest data took {round(end_time - start_time,2)} seconds")
    logger.info(f"starting web server...")

    """
    area_types = set()
    for sectors in forest.sectors_data.values():
        for sector in sectors:
            area_types.add(sector.json["area_type"])
    print(area_types)
    print("\n"*5)
    """


    web(forest)


