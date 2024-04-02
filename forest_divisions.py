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
    def __init__(self):
        pass

class Forestry:
    def __init__(self):
        pass