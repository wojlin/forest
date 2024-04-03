from typing import List
from tqdm import tqdm
import traceback
import logging
import json
import os

from forest_divisions import RDLP, ForestDistrict, Forestry, Sector
from utils import Fetcher, SingletonMeta


class ForestData(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger("forest")
        self.__cols_amount = 100
        self.__format = '{percentage:.0f}%|{bar}| {n_fmt}/{total_fmt} Elements | Elapsed: {elapsed} | Remaining: {remaining}'

        self.__rdlp: List[RDLP] = []
        self.__district: List[ForestDistrict] = []
        self.__forestry: List[Forestry] = []
        self.__sectors: List[Sector] = []

    @property
    def rdlp_data(self):
        return self.__rdlp

    @property
    def district_data(self):
        return self.__rdlp

    @property
    def forestry_data(self):
        return self.__rdlp

    def load_forest_data(self):
        self.logger.info("loading rdlp data...")
        self.__rdlp = self.get_rdlp()

        self.logger.info("loading district data...")
        self.__district = self.get_district()

        self.logger.info("loading forestry data...")
        self.__forestry = self.get_forestry()

    def get_rdlp(self) -> List[RDLP]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/rdlp"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data: dict = json.loads(file.read())
                    amount = len(data)
                    rdlp = []
                    with tqdm(total=amount, desc="reading rdlp", ncols=self.__cols_amount, unit_scale=True, unit="item",
                              bar_format=self.__format) as pbar:
                        for i in range(amount):
                            i = str(i)
                            rdlp.append(RDLP(data[i]["name"], data[i]["id"]))
                            pbar.update(1)
                    return rdlp
            except Exception as e:
                print(traceback.format_exc())

        self.logger.warning("rdlp information is missing. fetching resource...")

        content = Fetcher().get(
            "https://ogcapi.bdl.lasy.gov.pl/collections/rdlp/items?f=json&lang=en-US&skipGeometry=true")

        amount = len(content["features"])
        rdlp = []
        with tqdm(total=amount, desc="reading rdlp", ncols=self.__cols_amount, unit_scale=True, unit="item",
                  bar_format=self.__format) as pbar:
            for i in range(amount):
                item = content["features"][i]
                rdlp.append(RDLP(item['properties']['region_name'], int(item['properties']['region_cd'])))
                pbar.update(1)

        data_to_save = {}
        iter = 0
        for item in rdlp:
            data_to_save[iter] = {"name": item.name, "id": item.id}
            iter+=1

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

        self.logger.warning("rdlp information fetched!")

        return rdlp

    def get_district(self) -> List[ForestDistrict]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/forest_district"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data = json.loads(file.read())
                    amount = len(data)
                    district = []
                    with tqdm(total=amount, desc="reading rdlp", ncols=self.__cols_amount, unit_scale=True, unit="item",
                              bar_format=self.__format) as pbar:
                        for i in range(amount):
                            i = str(i)
                            district.append(ForestDistrict(data[str(i)]["name"], data[str(i)]["id"], data[str(i)]["id"], data[str(i)]["rdlp_id"]))
                            pbar.update(1)
                    return district
            except Exception as e:
                print(traceback.format_exc())

        self.logger.warning("district information is missing. fetching resource...")

        content = Fetcher().get("https://ogcapi.bdl.lasy.gov.pl/collections/nadlesnictwa/items"
                                "?f=json&lang=en-US&limit=10000&skipGeometry=true&offset=0")

        amount = len(content["features"])
        district = []
        with tqdm(total=amount, desc="reading rdlp", ncols=self.__cols_amount, unit_scale=True, unit="item",
                  bar_format=self.__format) as pbar:
            for i in range(amount):
                data = content["features"][i]["properties"]
                district.append(
                    ForestDistrict(data["inspectorate_name"], content["features"][i]["id"], data["inspectorate_cd"], data["region_cd"]))
                pbar.update(1)

        data_to_save = {}
        iter = 0
        for item in district:
            data_to_save[iter] = {"name": item.name,
                                          "id": item.id,
                                          "district_id": item.district_id,
                                          "rdlp_id": item.rdlp_id}
            iter+=1

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

        self.logger.warning("district information fetched!")

        return district

    def get_forestry(self) -> List[Forestry]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/forestry"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data = json.loads(file.read())
                    amount = len(data)
                    forestry = []
                    with tqdm(total=amount, desc="reading rdlp", ncols=self.__cols_amount, unit_scale=True, unit="item",
                              bar_format=self.__format) as pbar:
                        for i in range(amount):
                            i = str(i)
                            forestry_name = data[i]["name"]
                            item_id = data[i]["id"]
                            rdlp_id = data[i]["rdlp_id"]
                            district_id = data[i]["district_id"]
                            forestry_id = data[i]["forestry_id"]
                            forestry.append(Forestry(forestry_name, item_id, rdlp_id, district_id, forestry_id))
                            pbar.update(1)
                    return forestry
            except Exception as e:
                print(traceback.format_exc())

        self.logger.warning("forestry information is missing. fetching resource...")

        content = Fetcher().get("https://ogcapi.bdl.lasy.gov.pl/collections/lesnictwa/items"
                                "?f=json&lang=en-US&limit=10000&skipGeometry=true&offset=0")

        amount = len(content["features"])
        forestry = []
        with tqdm(total=amount, desc="reading rdlp", ncols=self.__cols_amount, unit_scale=True, unit="item",
                  bar_format=self.__format) as pbar:
            for i in range(amount):
                item = content["features"][i]
                forestry_name = item["properties"]["forest_range_name"]
                item_id = item["id"]
                address = str(item["properties"]["adress_forest"]).split("-")

                # address_forest 	01   -   01   -   1  -   01   - - -
                #                   ^        ^        ^      ^
                #               rdlp     district     ?      ?

                rdlp_id = int(address[0])
                district_id = int(address[1])
                forestry_id = int( str(address[2]) + str(address[3]) )

                forestry.append(Forestry(forestry_name, item_id, rdlp_id, district_id, forestry_id))
                pbar.update(1)

        data_to_save = {}
        iter = 0
        for item in forestry:
            data_to_save[iter] = {"name": item.name,
                                          "id": item.id,
                                          "district_id": item.district_id,
                                          "rdlp_id": item.rdlp_id,
                                          "forestry_id": item.forestry_id}
            iter+=1

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

        self.logger.warning("forestry information fetched!")

        return forestry

    def get_sectors(self):
        for rdlp in self.__rdlp:
            name: str = f"RDLP_{rdlp.name.lower().title()}_wydzielenia"
            url: str = f"https://ogcapi.bdl.lasy.gov.pl/collections/{name}/items?f=json&lang=en-US&limit=100&skipGeometry=true&offset=0"
            print(url)
            #content = Fetcher().get(url)