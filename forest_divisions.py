import logging
import ast
import os

from utils import Fetcher

class RDLP:
    def __init__(self, rdlp_name: str, id: int):
        self.__logger = logging.getLogger("forest")
        self.__name = rdlp_name
        self.__id = id

        root= os.path.dirname(os.path.abspath(__file__))
        self.__path = f"{root}/database/rdlp/rdlp{self.__id}.geo"

        self.__geometry = self.__get_geometry()

        self.__children = []

    def __repr__(self):
        return f"Regionalna Dyrekcja Lasów Państwowych \"{self.__name}\" \"{self.__id}\" geometry points: \"{len(self.__geometry)}\""

    def json(self):
        return {"name": self.__name, "id": self.__id, "geometry": self.__geometry}

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
    def children(self):
        return self.__children

    def __get_geometry(self):
        if os.path.isfile(self.__path):
            try:
                with open(self.__path, 'r') as file:
                    return ast.literal_eval(file.read())
            except Exception as e:
                print(e)

        #self.__logger.warning(f"geojson for rdlp \"{self.__id}\" \"{self.__name}\" is missing, fetching resource...")
        geometry = self.__fetch_geometry()
        self.__geometry = geometry
        self.__save_geometry()
        #self.__logger.warning(f"geojson for rdlp \"{self.__id}\" \"{self.__name}\" fetched!")
        return geometry

    def __fetch_geometry(self):
        content = Fetcher().get(f"https://ogcapi.bdl.lasy.gov.pl/collections/rdlp/items/{self.__id}")
        return content["geometry"]["coordinates"][0][0]

    def __save_geometry(self):
        with open(self.__path, 'w') as file:
            file.write(str(self.__geometry))


class ForestDistrict:
    def __init__(self, district_name: str, id: int,  district_id: id, rdlp_id: int):
        self.__logger = logging.getLogger("forest")

        self.__district_name = district_name
        self.__id = id
        self.__district_id = district_id
        self.__rdlp_id = rdlp_id

        root = os.path.dirname(os.path.abspath(__file__))
        self.__path = f"{root}/database/district/district_{self.__id}.geo"
        self.__geometry = self.__get_geometry()

        self.__children = []

    def __repr__(self):
        return f"Nadleśnictwo \"{self.__district_name}\" \"{self.__id}\" \"{self.__rdlp_id}-{self.__district_id}\" geometry points: \"{len(self.__geometry)}\""

    def json(self):
        return {"name": self.__district_name, "id": self.__id, "geometry": self.__geometry}

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

    @property
    def children(self):
        return self.__children

    def __get_geometry(self):
        if os.path.isfile(self.__path):
            try:
                with open(self.__path, 'r') as file:
                    return ast.literal_eval(file.read())
            except Exception as e:
                print(e)

        #self.__logger.warning(f"geojson for district \"{self.__rdlp_id}-{self.__district_id}\" \"{self.__district_name}\" is missing, fetching resource...")
        geometry = self.__fetch_geometry()
        self.__geometry = geometry
        self.__save_geometry()
        #self.__logger.warning(f"geojson for district \"{self.__rdlp_id}-{self.__district_id}\" \"{self.__district_name}\" fetched!")
        return geometry

    def __fetch_geometry(self):
        content = Fetcher().get(f"https://ogcapi.bdl.lasy.gov.pl/collections/nadlesnictwa/items/{self.__id}?f=json")
        return content["geometry"]["coordinates"][0][0]

    def __save_geometry(self):
        with open(self.__path, 'w') as file:
            file.write(str(self.__geometry))


class Forestry:
    def __init__(self, forestry_name: str, id: int, rdlp_id, district_id: int, forestry_id: int):
        self.__logger = logging.getLogger("forest")
        self.__forestry_name = forestry_name
        self.__id = id
        self.__rdlp_id = rdlp_id
        self.__district_id = district_id
        self.__forestry_id = forestry_id

        root = os.path.dirname(os.path.abspath(__file__))
        self.__path = f"{root}/database/forestry/forestry_{self.__id}.geo"
        self.__geometry = self.__get_geometry()

        self.__children = []

    def __repr__(self):
        return f"Leśnictwo \"{self.__forestry_name}\" \"{self.__id}\" \"{self.__rdlp_id}-{self.__district_id}-{self.__forestry_id}\" geometry points: \"{len(self.__geometry)}\""

    def json(self):
        return {"name": self.__forestry_name, "id": self.__id, "geometry": self.__geometry}

    @property
    def name(self):
        return self.__forestry_name

    @property
    def id(self):
        return self.__id

    @property
    def forestry_id(self):
        return self.__forestry_id

    @property
    def district_id(self):
        return self.__district_id

    @property
    def rdlp_id(self):
        return self.__rdlp_id

    @property
    def geometry(self):
        return self.__geometry

    @property
    def children(self):
        return self.__children

    def __get_geometry(self):
        if os.path.isfile(self.__path):
            try:
                with open(self.__path, 'r') as file:
                    return ast.literal_eval(file.read())
            except Exception as e:
                print(e)

        #self.__logger.warning(f"geojson for forestry \"{self.__rdlp_id}-{self.__district_id}-{self.__forestry_id}\" \"{self.__forestry_name}\" is missing, fetching resource...")
        geometry = self.__fetch_geometry()
        self.__geometry = geometry
        self.__save_geometry()
        #self.__logger.warning(f"geojson for forestry \"{self.__rdlp_id}-{self.__district_id}-{self.__forestry_id}\" \"{self.__forestry_name}\" fetched!")
        return geometry

    def __fetch_geometry(self):
        content = Fetcher().get(f"https://ogcapi.bdl.lasy.gov.pl/collections/lesnictwa/items/{self.__id}?f=json")
        return content["geometry"]["coordinates"][0][0]

    def __save_geometry(self):
        with open(self.__path, 'w') as file:
            file.write(str(self.__geometry))


class Sector:
    def __init__(self, sector_name, id, area_type:str, site_type: str, forest_function: str, species: str, species_age: int, rotat_age: int, year: int):
        self.__logger = logging.getLogger("forest")
        self.__sector_name = sector_name
        self.__id = id
        self.__area_type = area_type # rodzaj powierzchni  "https://www.lasy.gov.pl/pl/publikacje/copy_of_gospodarka-lesna/urzadzanie/iul/instrukcja-urzadzania-lasu-czesc-i-dokument-przed-korekta/@@download/file/Instrukcja%20urz%C4%85dzania%20lasu_cz%201.pdf"
        self.__site_type = site_type  # typ siedliskowy lasu  https://www.encyklopedialesna.pl/haslo/las-mieszany-swiezy-lmsw/
        self.__forest_function = forest_function  # funkcja lasu (kategorie ochronne) https://www.encyklopedialesna.pl/haslo/kategorie-lasow-ochronnych/
        self.__species = species  # gatunki drzew https://www.encyklopedialesna.pl/haslo/typ-drzewostanu-td/
        self.__species_age = species_age  # wiek drzew
        self.__rotat_age = rotat_age # wiek rębności
        self.__year = year # rok w którym zostały sporządzone dane
        



        root = os.path.dirname(os.path.abspath(__file__))
        self.__path = f"{root}/database/forestry_{self.__id}.geo"
        self.__geometry = self.__get_geometry()
        self.__save_geometry()