import logging
import colorlog

from forest_data import ForestData
from utils import Fetcher

if __name__ == "__main__":
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

    forest = ForestData()
    logger.info("loading rdlp data...")
    rdlp = forest.get_rdlp()

    logger.info("loading district data...")
    district = forest.get_district()

    logger.info("loading forestry data...")
    forestry = forest.get_forestry()

    """
    print()
    print()
    for item in rdlp:
        print(item)
    for item in district:
        print(item)
    for item in forestry:
        print(item)
    """

    #print(Fetcher().requests_done)


