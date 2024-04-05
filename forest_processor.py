import io
import requests
import osmium as o
import math
from typing import List
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.image as mpimg
import zlib

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from utils import Fetcher
from forest_divisions import Sector


class ForestProcessor:
    def __init__(self):
        pass

    def deg2tile(self, lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def fits_in_one_tile(self, min_lat, min_lon, max_lat, max_lon, zoom):
        top_left = self.deg2tile(max_lat, min_lon, zoom)
        bottom_right = self.deg2tile(min_lat, max_lon, zoom)
        return top_left == bottom_right

    def find_best_zoom(self, polygon):
        # Extract separate lists of x and y values
        lon_vals, lat_vals = zip(*polygon)

        # Find the bounding box
        min_lon, max_lon = min(lon_vals), max(lon_vals)
        min_lat, max_lat = min(lat_vals), max(lat_vals)

        for zoom in reversed(range(1, 20)):  # OSM zoom levels go from 0 to 19

            if self.fits_in_one_tile(min_lon, min_lat, max_lon, max_lat, zoom):
                return zoom, self.deg2tile(min_lat + (max_lat - min_lat) / 2, min_lon + (max_lon - min_lon) / 2, zoom)
        return None, None


    def process_pbf_data(self, pbf_data):
        class RoadHandler(o.SimpleHandler):
            def __init__(self):
                super(RoadHandler, self).__init__()
                self.roads = []

            def way(self, w):
                # Filter for various types of roads, paths, and tracks
                road_tags = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary',
                             'unclassified', 'residential', 'service', 'track', 'path', 'cycleway',
                             'footway', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link',
                             'tertiary_link', 'living_street', 'pedestrian', 'bridleway', 'steps']
                for tag in road_tags:
                    if tag in w.tags:
                        self.roads.append((w.id, tag, [(n.lat, n.lon) for n in w.nodes]))


        # Initialize the handler and apply it to the PBF data



        handler = RoadHandler()
        handler.apply_file("tile.pbf")

        # Example: print the roads extracted
        return handler.roads

    def get_tile_bounds(self, x, y, zoom):
        """
        Returns the latitudinal and longitudinal bounds of an OSM tile.

        Parameters:
        - x, y: Tile coordinates
        - zoom: Zoom level

        Returns:
        - (lat_min, lon_min, lat_max, lon_max): Tuple with the boundaries of the tile
        """

        n = 2.0 ** zoom
        lon_min = x / n * 360.0 - 180.0
        lon_max = (x + 1) / n * 360.0 - 180.0
        lat_min_rad = math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / n)))
        lat_max_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        lat_min = math.degrees(lat_min_rad)
        lat_max = math.degrees(lat_max_rad)

        return lon_min, lon_max, lat_min, lat_max

    def process_sector(self, sector: Sector, show_result=False):
        geometry: List[float, float] = sector.geometry

        zoom, tile_coords = processor.find_best_zoom(geometry)

        url_vector = f"https://basemaps.arcgis.com/arcgis/rest/services/OpenStreetMap_v2/VectorTileServer/tile/{zoom}/{tile_coords[0]}/{tile_coords[1]}.pbf"
        url_raster = f"https://b.tile-cyclosm.openstreetmap.fr/cyclosm/{zoom}/{tile_coords[0]}/{tile_coords[1]}.png"

        print(url_vector)
        print(url_raster)

        vector = Fetcher().raw_get(url_vector)
        raster = Fetcher().raw_get(url_raster)


        #with open("tile.pbf", 'wb') as file:
        #    file.write(vector)
        #self.process_pbf_data(vector)


        tile_bounds = self.get_tile_bounds(tile_coords[0], tile_coords[1], zoom)


        if show_result:
            polygon = Polygon(geometry, closed=True, edgecolor='r', facecolor='lightblue')

            fig, ax = plt.subplots()

            ax.set_xlim([tile_bounds[0], tile_bounds[1]])
            ax.set_ylim([tile_bounds[2], tile_bounds[3]])

            ax.add_patch(polygon)

            img = mpimg.imread(BytesIO(raster))


            ax.imshow(img, extent=[tile_bounds[0], tile_bounds[1], tile_bounds[2], tile_bounds[3]], alpha=0.7)
            ax.set_aspect(1.6)

            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.title('OSM Tile Overlay')
            plt.grid(True)
            plt.show()


if __name__ == "__main__":
    data = {
        "sector_name": "BDL_03_02_BRZESKO_2023",
        "id": 1,
        "address": "03-02-1-01-1     -a   -00",
        "silvicult": "S",
        "area_type": "D-STAN",
        "site_type": "LŁWYŻ",
        "stand_structure": "DRZEW",
        "forest_function": "GOSP",
        "spiecies": "OL",
        "species_age": 24,
        "rotation_age": 80,
        "year": 2023,
        "geometry": [
            [
                20.556537443227814,
                49.964953958516546
            ],
            [
                20.55610849689058,
                49.96511725846865
            ],
            [
                20.555817042604918,
                49.96533566594113
            ],
            [
                20.55572132527753,
                49.96552508501758
            ],
            [
                20.555685973899248,
                49.96569192067873
            ],
            [
                20.55556109338186,
                49.9658161399028
            ],
            [
                20.555534787217212,
                49.965835207259445
            ],
            [
                20.55547495049248,
                49.96587856734682
            ],
            [
                20.555423250264287,
                49.96595798773523
            ],
            [
                20.555425508413467,
                49.96602804700573
            ],
            [
                20.55540099872812,
                49.966111511444986
            ],
            [
                20.555357221121085,
                49.96612082597418
            ],
            [
                20.555248472832155,
                49.965975267150796
            ],
            [
                20.555210446429978,
                49.96602886156511
            ],
            [
                20.554651757128834,
                49.96617032256604
            ],
            [
                20.55409659526753,
                49.966139883749044
            ],
            [
                20.5541815885141,
                49.96625391125403
            ],
            [
                20.55416043221375,
                49.96651952730316
            ],
            [
                20.553298340193884,
                49.96733679070817
            ],
            [
                20.553298223923342,
                49.96733751205505
            ],
            [
                20.553299879715865,
                49.967336950037776
            ],
            [
                20.55341320821086,
                49.96738221857992
            ],
            [
                20.55343299191857,
                49.96739014121677
            ],
            [
                20.553465774046465,
                49.967403198202305
            ],
            [
                20.553700085883886,
                49.967610148276336
            ],
            [
                20.553958185372036,
                49.96759409422088
            ],
            [
                20.554540090809056,
                49.96755786468212
            ],
            [
                20.55455247986404,
                49.967557068814344
            ],
            [
                20.5546678512696,
                49.96739725863144
            ],
            [
                20.554888008684856,
                49.96709118589545
            ],
            [
                20.554904027320724,
                49.96706883760859
            ],
            [
                20.55497522805806,
                49.96696684254871
            ],
            [
                20.55505308693063,
                49.966855041009545
            ],
            [
                20.555374805464353,
                49.96639375046637
            ],
            [
                20.55539040246853,
                49.96637131778849
            ],
            [
                20.555641086948153,
                49.96608219908293
            ],
            [
                20.5562499835926,
                49.96533507603501
            ],
            [
                20.556637768582906,
                49.96498104377129
            ],
            [
                20.556636769413295,
                49.96498033739126
            ],
            [
                20.556537443227814,
                49.964953958516546
            ]
        ]
    }

    sector = Sector(sector_name=data["sector_name"], id=data["id"], address=data["address"],
                    silvicult=data["silvicult"], area_type=data["area_type"], site_type=data["site_type"],
                    stand_structure=data["stand_structure"], forest_function=data["forest_function"],
                    species=data["spiecies"], species_age=data["species_age"], rotat_age=data["rotation_age"],
                    year=data["year"], geometry=data["geometry"])

    processor = ForestProcessor()
    geometry = []
    processor.process_sector(sector, show_result=True)

    """
    polygon = [[51.5, 0], [51.5, 0.1], [51.4, 0.1], [51.4, 0]]

    zoom, tile_coords = processor.find_minimum_covering_tile(polygon)
    zoom -= 1
    if zoom is not None:
        print(f"Minimum covering tile: Zoom: {zoom}, X: {tile_coords[0]}, Y: {tile_coords[1]}")
    else:
        print("Couldn't find a single tile covering the polygon at the considered zoom levels.")


    url = f"https://basemaps.arcgis.com/arcgis/rest/services/OpenStreetMap_v2/VectorTileServer/tile/{zoom}/{tile_coords[0]}/{tile_coords[1]}.pbf"

    content = Fetcher().raw_get(url)
    roads = processor.process_pbf_data(content)
    """
