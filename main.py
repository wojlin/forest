import logging
import colorlog

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

    forest = ForestData()

    forest.load_forest_data()

    web(forest)


    #sectors = forest.get_sectors()

    #print(Fetcher().requests_done)


