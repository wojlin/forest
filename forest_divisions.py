import ast
import os

from utils import Fetcher

class RDLP:
    def __init__(self, rdlp_name: str, rdlp_id: int):
        self.__name = rdlp_name
        self.__id = rdlp_id

        root= os.path.dirname(os.path.abspath(__file__))
        self.__path = f"{root}/database/rdlp{self.__id}.geo"

        self.__geometry = self.__get_geometry()
        self.__save_geometry()

    def __repr__(self):
        return f"Regionalna Dyrekcja Lasów Państwowych \"{self.__name}\" \"{self.__id}\" geometry points: \"{len(self.__geometry)}\""

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def geometry(self):
        return self.__geometry

    @property
    def path(self):
        return self.__path

    def __get_geometry(self):
        if os.path.isfile(self.__path):
            try:
                with open(self.__path, 'r') as file:
                    return ast.literal_eval(file.read())
            except Exception as e:
                print(e)

        print(f"geojson for rdlp \"{self.__id}\" \"{self.__name}\" is missing, fetching resource...")
        geometry = self.__fetch_geometry()
        print(f"geojson for rdlp \"{self.__id}\" \"{self.__name}\" fetched!")
        return geometry

    def __fetch_geometry(self):
        content = Fetcher().get(f"https://ogcapi.bdl.lasy.gov.pl/collections/rdlp/items/{self.__id}")
        return content["geometry"]["coordinates"][0][0]

    def __save_geometry(self):
        with open(self.__path, 'w') as file:
            file.write(str(self.__geometry))


class ForestDistrict:
    def __init__(self, district_name: str, id: int,  district_id: id, rdlp_id: int):
        self.__district_name = district_name
        self.__id = id
        self.__district_id = district_id
        self.__rdlp_id = rdlp_id

        root = os.path.dirname(os.path.abspath(__file__))
        self.__path = f"{root}/database/district_{self.__id}.geo"
        self.__geometry = []
        self.__geometry = self.__get_geometry()
        self.__save_geometry()

    def __repr__(self):
        return f"Nadleśnictwo \"{self.__district_name}\" \"{self.__id}\" \"{self.__rdlp_id}-{self.__district_id}\" geometry points: \"{len(self.__geometry)}\""

    @property
    def name(self):
        return self.__district_name

    @property
    def id(self):
        return self.__id

    @property
    def district_id(self):
        return self.__district_id

    @property
    def rdlp_id(self):
        return self.__rdlp_id

    @property
    def geometry(self):
        return self.__geometry

    def __get_geometry(self):
        if os.path.isfile(self.__path):
            try:
                with open(self.__path, 'r') as file:
                    return ast.literal_eval(file.read())
            except Exception as e:
                print(e)

        print(f"geojson for district \"{self.__rdlp_id}-{self.__district_id}\" \"{self.__district_name}\" is missing, fetching resource...")
        geometry = self.__fetch_geometry()
        print(f"geojson for district \"{self.__rdlp_id}-{self.__district_id}\" \"{self.__district_name}\" fetched!")
        return geometry

    def __fetch_geometry(self):
        content = Fetcher().get(f"https://ogcapi.bdl.lasy.gov.pl/collections/nadlesnictwa/items/{self.__id}?f=json")
        return content["geometry"]["coordinates"][0][0]

    def __save_geometry(self):
        with open(self.__path, 'w') as file:
            file.write(str(self.__geometry))


class Forestry:
    def __init__(self):
        pass