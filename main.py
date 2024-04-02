import json
import os

from utils import Fetcher
from forest_divisions import RDLP, ForestDistrict, Forestry


def get_rdlp():
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

    content = Fetcher().get("https://ogcapi.bdl.lasy.gov.pl/collections/rdlp/items?f=json&lang=en-US&skipGeometry=true")
    items = [element for element in content["features"]]
    rdlp = [RDLP(item['properties']['region_name'], int(item['properties']['region_cd'])) for item in items]

    data_to_save = {}
    for item in rdlp:
        data_to_save[item.id] = {"name": item.name, "id": item.id}

    with open(path, 'w') as file:
        file.write(json.dumps(data_to_save))

    print("rdlp information fetched!")

    return rdlp


if __name__ == "__main__":
    rdlp = get_rdlp()
    for item in rdlp:
        print(item)

    print(Fetcher().requests_done)


