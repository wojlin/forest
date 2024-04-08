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
        self.__logger = logging.getLogger("forest")
        self.__cols_amount = 20
        self.__format = '{percentage:.0f}%|{bar}| {n_fmt}/{total_fmt} Elements | Elapsed: {elapsed} | Remaining: {remaining}'

        self.__rdlp: Dict[str, ForestDistrict] = {}
        self.__district: Dict[str, ForestDistrict] = {}
        self.__forestry: Dict[str, ForestDistrict] = {}
        self.__sectors: Dict[str, List[Sector]] = {}

        self.__load_forest_data()

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

    def __save_pickle(self):
        pass
        #with open("save.p", "wb") as file:
        #    pickle.dump(self, file)

    def __load_pickle(self):
        #with open("save.p", "rb") as f:
        #    self = pickle.load(f)
        pass

    def __load_forest_data(self):
        self.__logger.info("loading rdlp data...")
        self.__rdlp = self.__load_rdlp()

        self.__logger.info("loading district data...")
        self.__district = self.__load_district()

        self.__logger.info("loading forestry data...")
        self.__forestry = self.__load_forestry()

        self.__logger.info("loading sectors data...")
        self.__sectors = self.__load_sectors()

        self.__logger.info("connecting data points...")
        self.__connect_data_points()

        self.__logger.info("all data is ready!")

    def __connect_data_points(self):
        amount = len(self.__forestry) * len(self.__district)
        done = 0
        progress = Progress()
        task_id = progress.add_task("", total=amount)

        with progress:


            for forestry in self.__forestry.values():
                for district in self.__district.values():

                    progress_percentage = (done + 1) / amount
                    bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                    bar_style = "[green]" if progress_percentage >= 0.8 else bar_style
                    done += 1
                    progress.update(task_id, advance=1,
                                    description=f"[white]{'processing forestry:'.ljust(self.__cols_amount)} {bar_style}{int(done) + 1}[white]/[green]{amount}",
                                    bar_style=bar_style)

                    if int(district.rdlp_id) == int(forestry.rdlp_id):
                        if int(district.district_id) == int(forestry.district_id):
                            district.children.append(forestry)

        amount = len(self.__district) * len(self.__rdlp)
        done = 0
        progress = Progress()
        task_id = progress.add_task("", total=amount)
        with progress:
            for rdlp in self.__rdlp.values():
                for district in self.__district.values():

                    progress_percentage = (done + 1) / amount
                    bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                    bar_style = "[green]" if progress_percentage >= 0.8 else bar_style
                    done += 1
                    progress.update(task_id, advance=1,
                                    description=f"[white]{'processing districts:'.ljust(self.__cols_amount)} {bar_style}{int(done) + 1}[white]/[green]{amount}",
                                    bar_style=bar_style)

                    if int(rdlp.id) == int(district.rdlp_id):
                        rdlp.children.append(district)


        amount = sum([len(sector) for sector in self.__sectors.values()])
        done = 0
        missing = 0
        progress = Progress()
        task_id = progress.add_task("", total=amount)
        with progress:

            progress_percentage = (done + 1) / amount
            bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
            bar_style = "[green]" if progress_percentage >= 0.8 else bar_style
            progress.update(task_id, advance=0,
                            description=f"[white]{'processing sectors:'.ljust(self.__cols_amount)} {bar_style}{int(done) + 1}[white]/[green]{amount}",
                            bar_style=bar_style)

            for name, sectors in self.__sectors.items():
                for sector in sectors:
                    key = f"{int(sector.rdlp_id)}-{int(sector.district_id)}-{int(sector.forestry_id)}"
                    if key in self.__forestry:
                        self.__forestry[key].children.append(sector)
                    else:
                        missing += 1

                    progress_percentage = (done + 1) / amount
                    bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                    bar_style = "[green]" if progress_percentage >= 0.8 else bar_style
                    done += 1
                    progress.update(task_id, advance=1,
                                    description=f"[white]{'processing sectors:'.ljust(self.__cols_amount)} {bar_style}{int(done) + 1}[white]/[green]{amount}",
                                    bar_style=bar_style)

            self.__logger.warning(f"{missing} missing sectors found!")

    @staticmethod
    def normalize_rdlp_name(name: str):
        return unidecode(f"RDLP_{name.lower().title().replace(' ', '_')}_wydzielenia")

    def __load_rdlp(self) -> Dict[str, RDLP]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/rdlp.json"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data: dict = json.loads(file.read())
                    amount = len(data)
                    rdlp = {}




                    with Progress() as progress:
                        task_id = progress.add_task("[red]Scraping", total=amount)
                        for i in range(amount):
                            progress_percentage = (i + 1) / amount
                            bar_style = "[yellow]" if progress_percentage >= 0.5 else "[red]"
                            bar_style = "[green]" if progress_percentage >= 0.8 else bar_style
                            i = str(i)
                            new_rdlp = RDLP(data[i]["name"], data[i]["id"])
                            rdlp[str(int(new_rdlp.id))] = new_rdlp
                            progress.update(task_id, advance=1,
                                            description=f"[white]{'processing rdlp:'.ljust(self.__cols_amount)} {bar_style}{int(i) + 1}[white]/[green]{amount}",
                                            bar_style=bar_style)

                    return rdlp

            except Exception as e:
                print(traceback.format_exc())

        self.__logger.warning("rdlp information is missing. fetching resource...")

        content = Fetcher().get(
            "https://ogcapi.bdl.lasy.gov.pl/collections/rdlp/items?f=json&lang=en-US&skipGeometry=true")

        amount = len(content["features"])
        rdlp = {}

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
                new_rdlp = RDLP(item['properties']['region_name'], int(item['properties']['region_cd']))
                rdlp[str(int(new_rdlp.id))] = new_rdlp



        data_to_save = {}
        iter = 0
        for item in rdlp.values():
            data_to_save[iter] = {"name": item.name, "id": item.id}
            iter+=1

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

        self.__logger.warning("rdlp information fetched!")

        return rdlp

    def __load_district(self) -> Dict[str, ForestDistrict]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/district.json"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data = json.loads(file.read())
                    amount = len(data)
                    district = {}

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

                            new_district = ForestDistrict(data[str(i)]["name"], data[str(i)]["id"], data[str(i)]["district_id"],
                                           data[str(i)]["rdlp_id"])
                            key = f"{int(new_district.rdlp_id)}-{int(new_district.district_id)}"
                            district[key] = new_district
                    return district
            except Exception as e:
                print(traceback.format_exc())

        self.__logger.warning("district information is missing. fetching resource...")

        content = Fetcher().get("https://ogcapi.bdl.lasy.gov.pl/collections/nadlesnictwa/items"
                                "?f=json&lang=en-US&limit=10000&skipGeometry=true&offset=0")

        amount = len(content["features"])
        district = {}

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
                new_district = ForestDistrict(data["inspectorate_name"], content["features"][i]["id"], data["inspectorate_cd"],
                                   data["region_cd"])

                key = f"{int(new_district.rdlp_id)}-{int(new_district.district_id)}"
                district[key] = new_district



        data_to_save = {}
        iter = 0
        for item in district.values():
            data_to_save[iter] = {"name": item.name,
                                          "id": item.id,
                                          "district_id": item.district_id,
                                          "rdlp_id": item.rdlp_id}
            iter+=1

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

        self.__logger.warning("district information fetched!")

        return district

    def __load_forestry(self) -> Dict[str, Forestry]:
        root = os.path.dirname(os.path.abspath(__file__))
        path = f"{root}/database/forestry.json"
        if os.path.isfile(path):
            try:
                with open(path, 'r') as file:
                    data = json.loads(file.read())
                    amount = len(data)
                    forestry = {}

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

                            new_forestry = Forestry(forestry_name, item_id, rdlp_id, district_id, forestry_id)
                            key = f"{int(new_forestry.rdlp_id)}-{int(new_forestry.district_id)}-{int(new_forestry.forestry_id)}"
                            forestry[key] = new_forestry


                    return forestry
            except Exception as e:
                print(traceback.format_exc())

        self.__logger.warning("forestry information is missing. fetching resource...")

        content = Fetcher().get("https://ogcapi.bdl.lasy.gov.pl/collections/lesnictwa/items"
                                "?f=json&lang=en-US&limit=10000&skipGeometry=true&offset=0")

        amount = len(content["features"])
        forestry = {}

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


                new_forestry = Forestry(forestry_name, item_id, rdlp_id, district_id, forestry_id)
                key = f"{int(new_forestry.rdlp_id)}-{int(new_forestry.district_id)}-{int(new_forestry.forestry_id)}"
                forestry[key] = new_forestry


        data_to_save = {}
        iter = 0
        for item in forestry.values():
            data_to_save[iter] = {"name": item.name,
                                          "id": item.id,
                                          "district_id": item.district_id,
                                          "rdlp_id": item.rdlp_id,
                                          "forestry_id": item.forestry_id}
            iter+=1

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

        self.__logger.warning("forestry information fetched!")

        return forestry

    def __load_sectors(self) -> Dict[str, List[Sector]]:

        all_sectors: Dict[str, List[Sector]] = {}

        for rdlp in self.__rdlp.values():
            name: str = self.normalize_rdlp_name(rdlp.name)
            root = os.path.dirname(os.path.abspath(__file__))
            path = f"{root}/database/{name}.json"

            ### read
            if os.path.isfile(path):
                self.__logger.warning(f"reading {name} data...")
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

                                item = data[name][i]


                                sector_name = item["sector_name"]
                                item_id = item["id"]
                                silvicult = item["silvicult"]
                                area_type = item["area_type"]
                                stand_stru = item["stand_structure"]
                                species_cd = item["spiecies"]
                                spec_age = item["species_age"]
                                adr_for = item["address"]
                                site_type = item["site_type"]
                                forest_fun = item["forest_function"]
                                rotat_age = item["rotation_age"]
                                a_year = item["year"]
                                geometry = item["geometry"]

                                sector = Sector(sector_name=sector_name,
                                                id=item_id,
                                                address=adr_for,
                                                silvicult=silvicult,
                                                area_type=area_type,
                                                site_type=site_type,
                                                stand_structure=stand_stru,
                                                forest_function=forest_fun,
                                                species=species_cd,
                                                species_age=spec_age,
                                                rotat_age=rotat_age,
                                                year=a_year,
                                                geometry=geometry)

                                sectors[name].append(sector)
                        all_sectors[name] = sectors[name]
                    continue

                except Exception as e:
                    print(traceback.format_exc())

            ### fetch

            self.__logger.warning(f"sectors information for {name} is missing. fetching resource...")


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
            self.__logger.warning(f"fetched sectors for {name}!")


        self.__logger.warning("sectors information fetched!")


        return all_sectors

