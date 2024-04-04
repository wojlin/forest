from rich.progress import Progress
from unidecode import unidecode
from typing import List, Dict
import traceback
import logging
import json
import os

from forest_divisions import RDLP, ForestDistrict, Forestry, Sector
from utils import Fetcher, SingletonMeta


class ForestData(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger("forest")
        self.__cols_amount = 20
        self.__format = '{percentage:.0f}%|{bar}| {n_fmt}/{total_fmt} Elements | Elapsed: {elapsed} | Remaining: {remaining}'

        self.__rdlp: List[RDLP] = []
        self.__district: List[ForestDistrict] = []
        self.__forestry: List[Forestry] = []
        self.__sectors: Dict[str, List[Sector]] = {}


    @property
    def rdlp_data(self):
        return self.__rdlp

    @property
    def district_data(self):
        return self.__district

    @property
    def forestry_data(self):
        return self.__forestry

    @property
    def sectors_data(self):
        return self.__sectors

    def load_forest_data(self):
        self.logger.info("loading rdlp data...")
        self.__rdlp = self.get_rdlp()




        self.logger.info("loading district data...")
        self.__district = self.get_district()

        self.logger.info("loading forestry data...")
        self.__forestry = self.get_forestry()

        self.logger.info("connecting data points...")
        self.connect_data_points()

        self.logger.info("loading sectors data...")
        #self.__sectors = self.get_sectors()

        self.logger.info("all data is ready!")
        


    def connect_data_points(self):
        amount = len(self.__forestry) * len(self.__district) + len(self.__district) * len(self.__rdlp)
        done = 0
        progress = Progress()
        task_id = progress.add_task("", total=amount)

        with progress:
            for forestry in self.__forestry:
                for district in self.__district:

                    progress_percentage = (done + 1) / amount
                    bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                    bar_style = "[green]" if progress_percentage >= 0.8 else bar_style
                    done += 1
                    progress.update(task_id, advance=1,
                                    description=f"[white]{'processing data:'.ljust(self.__cols_amount)} {bar_style}{int(done) + 1}[white]/[green]{amount}",
                                    bar_style=bar_style)

                    if int(district.rdlp_id) == int(forestry.rdlp_id):
                        if int(district.district_id) == int(forestry.district_id):
                            district.children.append(forestry)

            for rdlp in self.__rdlp:
                for district in self.__district:

                    progress_percentage = (done + 1) / amount
                    bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                    bar_style = "[green]" if progress_percentage >= 0.8 else bar_style
                    done += 1
                    progress.update(task_id, advance=1,
                                    description=f"[white]{'processing data:'.ljust(self.__cols_amount)} {bar_style}{int(done) + 1}[white]/[green]{amount}",
                                    bar_style=bar_style)

                    if int(rdlp.id) == int(district.rdlp_id):
                        rdlp.children.append(district)

    def get_rdlp(self) -> List[RDLP]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/rdlp.json"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data: dict = json.loads(file.read())
                    amount = len(data)
                    rdlp = []




                    with Progress() as progress:
                        task_id = progress.add_task("[red]Scraping", total=amount)
                        for i in range(amount):
                            progress_percentage = (i + 1) / amount
                            bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                            bar_style = "[green]" if progress_percentage >= 0.8 else bar_style
                            i = str(i)
                            rdlp.append(RDLP(data[i]["name"], data[i]["id"]))
                            progress.update(task_id, advance=1,
                                            description=f"[white]{'processing rdlp:'.ljust(self.__cols_amount)} {bar_style}{int(i) + 1}[white]/[green]{amount}",
                                            bar_style=bar_style)



                    return rdlp
            except Exception as e:
                print(traceback.format_exc())

        self.logger.warning("rdlp information is missing. fetching resource...")

        content = Fetcher().get(
            "https://ogcapi.bdl.lasy.gov.pl/collections/rdlp/items?f=json&lang=en-US&skipGeometry=true")

        amount = len(content["features"])
        rdlp = []

        progress = Progress()
        task_id = progress.add_task("", total=amount)

        with progress:
            for i in range(amount):
                progress_percentage = (i + 1) / amount
                bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                bar_style = "[green]" if progress_percentage >= 0.8 else bar_style

                progress.update(task_id, advance=1,
                                description=f"[white]{'downloading rdlp:'.ljust(self.__cols_amount)} {bar_style}{i + 1}[white]/[green]{amount}",
                                bar_style=bar_style)

                item = content["features"][i]
                rdlp.append(RDLP(item['properties']['region_name'], int(item['properties']['region_cd'])))



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
        path = f"{root}/database/district.json"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data = json.loads(file.read())
                    amount = len(data)
                    district = []

                    progress = Progress()
                    task_id = progress.add_task("", total=amount)

                    with progress:
                        for i in range(amount):
                            progress_percentage = (i + 1) / amount
                            bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                            bar_style = "[green]" if progress_percentage >= 0.8 else bar_style

                            progress.update(task_id, advance=1,
                                            description=f"[white]{'processing district:'.ljust(self.__cols_amount)} {bar_style}{i + 1}[white]/[green]{amount}",
                                            bar_style=bar_style)

                            i = str(i)
                            district.append(ForestDistrict(data[str(i)]["name"], data[str(i)]["id"], data[str(i)]["district_id"],
                                                           data[str(i)]["rdlp_id"]))



                    return district
            except Exception as e:
                print(traceback.format_exc())

        self.logger.warning("district information is missing. fetching resource...")

        content = Fetcher().get("https://ogcapi.bdl.lasy.gov.pl/collections/nadlesnictwa/items"
                                "?f=json&lang=en-US&limit=10000&skipGeometry=true&offset=0")

        amount = len(content["features"])
        district = []

        progress = Progress()
        task_id = progress.add_task("", total=amount)

        with progress:
            for i in range(amount):
                progress_percentage = (i + 1) / amount
                bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                bar_style = "[green]" if progress_percentage >= 0.8 else bar_style

                progress.update(task_id, advance=1,
                                description=f"[white]{'downloading district:'.ljust(self.__cols_amount)} {bar_style}{i + 1}[white]/[green]{amount}",
                                bar_style=bar_style)

                data = content["features"][i]["properties"]
                district.append(
                    ForestDistrict(data["inspectorate_name"], content["features"][i]["id"], data["inspectorate_cd"],
                                   data["region_cd"]))



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
        path = f"{root}/database/forestry.json"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data = json.loads(file.read())
                    amount = len(data)
                    forestry = []

                    progress = Progress()
                    task_id = progress.add_task("", total=amount)

                    with progress:
                        for i in range(amount):
                            progress_percentage = (i + 1) / amount
                            bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                            bar_style = "[green]" if progress_percentage >= 0.8 else bar_style

                            progress.update(task_id, advance=1,
                                            description=f"[white]{'processing forestry:'.ljust(self.__cols_amount)} {bar_style}{i + 1}[white]/[green]{amount}",
                                            bar_style=bar_style)

                            i = str(i)
                            forestry_name = data[i]["name"]
                            item_id = data[i]["id"]
                            rdlp_id = data[i]["rdlp_id"]
                            district_id = data[i]["district_id"]
                            forestry_id = data[i]["forestry_id"]
                            forestry.append(Forestry(forestry_name, item_id, rdlp_id, district_id, forestry_id))


                    return forestry
            except Exception as e:
                print(traceback.format_exc())

        self.logger.warning("forestry information is missing. fetching resource...")

        content = Fetcher().get("https://ogcapi.bdl.lasy.gov.pl/collections/lesnictwa/items"
                                "?f=json&lang=en-US&limit=10000&skipGeometry=true&offset=0")

        amount = len(content["features"])
        forestry = []

        progress = Progress()
        task_id = progress.add_task("", total=amount)

        with progress:
            for i in range(amount):
                progress_percentage = (i + 1) / amount
                bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                bar_style = "[green]" if progress_percentage >= 0.8 else bar_style

                progress.update(task_id, advance=1,
                                description=f"[white]{'downloading forestry:'.ljust(self.__cols_amount)} {bar_style}{i + 1}[white]/[green]{amount}",
                                bar_style=bar_style)

                item = content["features"][i]
                forestry_name = item["properties"]["forest_range_name"]
                item_id = item["id"]
                address = str(item["properties"]["adress_forest"]).split("-")

                # address_forest 	01   -   01   -   1  -   01   - - -
                #                   ^        ^        ^      ^
                #               rdlp     district     ?      ?

                rdlp_id = int(address[0])
                district_id = int(address[1])
                forestry_id = int(str(address[2]) + str(address[3]))

                forestry.append(Forestry(forestry_name, item_id, rdlp_id, district_id, forestry_id))



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

    def get_sectors(self) -> Dict[str, List[Sector]]:

        all_sectors: Dict[str, List[Sector]] = {}

        for rdlp in self.__rdlp:
            name: str = unidecode(f"RDLP_{rdlp.name.lower().title()}_wydzielenia")
            root = os.path.dirname(os.path.abspath(__file__))
            path = f"{root}/database/{name}.json"

            ### read
            if os.path.isfile(path):
                self.logger.warning(f"reading {name} data...")
                try:
                    with open(path, 'r') as file:
                        data = json.loads(file.read())
                        amount = len(data[name])
                        sectors = {name: []}

                        progress = Progress()
                        task_id = progress.add_task("", total=amount)

                        with progress:
                            for i in range(amount):
                                progress_percentage = (i + 1) / amount
                                bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                                bar_style = "[green]" if progress_percentage >= 0.8 else bar_style

                                progress.update(task_id, advance=1,
                                                description=f"[white]{'processing forestry:'.ljust(self.__cols_amount)} {bar_style}{i + 1}[white]/[green]{amount}",
                                                bar_style=bar_style)
                                sectors[name].append(data[name][i])
                        all_sectors[name] = sectors[name]
                    continue

                except Exception as e:
                    print(traceback.format_exc())

            ### fetch

            self.logger.warning(f"sectors information for {name} is missing. fetching resource...")


            sectors = {name: []}

            limit = 1
            offset = 0
            url: str = f"https://ogcapi.bdl.lasy.gov.pl/collections/{name}/items?f=json&lang=en-US&limit={limit}&skipGeometry=true&offset={offset}"

            content = Fetcher().get(url)
            total_amount = content["numberMatched"]


            total_left = total_amount
            limit = 100
            offset = 0

            progress = Progress()
            task_id = progress.add_task("", total=total_amount)

            with progress:
                while total_left > 0:
                    url: str = f"https://ogcapi.bdl.lasy.gov.pl/collections/{name}/items?f=json&lang=en-US&limit={limit}&skipGeometry=false&offset={offset}"
                    content = Fetcher().get(url)

                    amount = len(content["features"])

                    for i in range(amount):
                        item = content["features"][i]
                        sector_name = item["properties"]["nazwa"]
                        item_id = item["id"]
                        silvicult = item["properties"]["silvicult"]
                        area_type = item["properties"]["area_type"]
                        stand_stru = item["properties"]["stand_stru"]
                        species_cd = item["properties"]["species_cd"]
                        spec_age = item["properties"]["spec_age"]
                        adr_for = item["properties"]["adr_for"]
                        site_type = item["properties"]["site_type"]
                        forest_fun = item["properties"]["forest_fun"]
                        rotat_age  = item["properties"]["rotat_age"]
                        a_year = item["properties"]["a_year"]
                        geometry = item["geometry"]["coordinates"][0][0]

                        sector = Sector(sector_name=sector_name,
                                        id= item_id,
                                        address= adr_for,
                                        silvicult = silvicult,
                                        area_type=area_type,
                                        site_type=site_type,
                                        stand_structure = stand_stru,
                                        forest_function=forest_fun,
                                        species=species_cd,
                                        species_age=spec_age,
                                        rotat_age=rotat_age,
                                        year=a_year,
                                        geometry = geometry)


                        sectors[name].append(sector)

                    offset += limit
                    total_left -= limit

                    progress_percentage = ( (total_amount- total_left)) / total_amount
                    bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                    bar_style = "[green]" if progress_percentage >= 0.8 else bar_style

                    progress.update(task_id, advance=limit,
                                    description=f"[white]downloading {name} {bar_style}{ total_amount - total_left}[white]/[green]{total_amount}",
                                    bar_style=bar_style)

            data_to_save = {name: []}
            for item in sectors[name]:
                data_to_save[name].append(item.json)

            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data_to_save, file, indent=4, ensure_ascii=False)

            all_sectors[name] = list(sectors[name])
            self.logger.warning(f"fetched sectors for {name}!")


        self.logger.warning("sectors information fetched!")


        return all_sectors

