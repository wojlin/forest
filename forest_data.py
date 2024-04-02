from typing import List
import json
import os

from forest_divisions import RDLP, ForestDistrict, Forestry
from utils import Fetcher


class ForestData:
    def __init__(self):
        pass

    def get_rdlp(self) -> List[RDLP]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/rdlp"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data = json.loads(file.read())
                    return [RDLP(data[item]["name"], data[item]["id"]) for item in data]
            except Exception as e:
                print(e)

        print("rdlp information is missing. fetching resource...")

        content = Fetcher().get(
            "https://ogcapi.bdl.lasy.gov.pl/collections/rdlp/items?f=json&lang=en-US&skipGeometry=true")
        items = [element for element in content["features"]]
        rdlp = [RDLP(item['properties']['region_name'], int(item['properties']['region_cd'])) for item in items]

        data_to_save = {}
        for item in rdlp:
            data_to_save[item.id] = {"name": item.name, "id": item.id}

        with open(path, 'w') as file:
            file.write(json.dumps(data_to_save))

        print("rdlp information fetched!")

        return rdlp

    def get_district(self) -> List[ForestDistrict]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/forest_district"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data = json.loads(file.read())
                    return [
                        ForestDistrict(data[item]["name"], data[item]["id"], data[item]["id"], data[item]["rdlp_id"])
                        for item in data]
            except Exception as e:
                print(e)

        print("district information is missing. fetching resource...")

        content = Fetcher().get("https://ogcapi.bdl.lasy.gov.pl/collections/nadlesnictwa/items"
                                "?f=json&lang=en-US&limit=10000&skipGeometry=true&offset=0")

        district = []
        for item in content["features"]:
            data = item["properties"]
            district.append(
                ForestDistrict(data["inspectorate_name"], item["id"], data["inspectorate_cd"], data["region_cd"]))

        data_to_save = {}
        for item in district:
            data_to_save[f"{item.id}"] = {"name": item.name,
                                          "id": item.id,
                                          "district_id": item.district_id,
                                          "rdlp_id": item.rdlp_id}

        with open(path, 'w') as file:
            file.write(json.dumps(data_to_save))

        print("district information fetched!")

        return district

    def get_forestry(self) -> List[Forestry]:
        pass