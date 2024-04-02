import json
import os

from forest_data import ForestData
from utils import Fetcher

if __name__ == "__main__":
    forest = ForestData()
    rdlp = forest.get_rdlp()
    for item in rdlp:
        print(item)
    district = forest.get_district()
    for item in district:
        print(item)

    print(Fetcher().requests_done)


