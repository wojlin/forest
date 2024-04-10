from flask import Flask, render_template, jsonify
from forest_data import ForestData


class web:
    def __init__(self, forest):
        # Create an instance of the Flask class
        self.forest: ForestData = forest
        self.app = Flask("forest")
        self.setup_routes()

        self.app.run(host="localhost", port=2137, debug=False)

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/get_rdlp')
        def get_rdlp():
            data = {}
            for i, element in self.forest.rdlp_data.items():
                data[i] = element.json()
            return jsonify(data)

        @self.app.route('/get_district_from_rdlp/<rdlp_id>')
        def get_district_from_rdlp(rdlp_id: int):
            for rdlp in self.forest.rdlp_data.values():
                if int(rdlp.id) == int(rdlp_id):
                    data = {}
                    for i, element in enumerate(rdlp.children):
                        data[i] = element.json()

                    return jsonify(data)

            return jsonify({"status": "error"})

        @self.app.route('/get_forestry_from_district/<rdlp_id>/<district_id>')
        def get_forestry_from_district(rdlp_id:int, district_id: int):
            for rdlp in self.forest.rdlp_data.values():
                if int(rdlp.id) == int(rdlp_id):
                    for district in rdlp.children:
                        if int(district.district_id) == int(district_id):
                            data = {}
                            for i, element in enumerate(district.children):
                                data[i] = element.json()

                            return jsonify(data)

            return jsonify({"status": "error"})

        @self.app.route('/get_sector_from_forestry/<rdlp_id>/<district_id>/<forestry_id>')
        def get_sector_from_forestry(rdlp_id: int, district_id: int, forestry_id: int):
            for rdlp in self.forest.rdlp_data.values():
                if int(rdlp.id) == int(rdlp_id):
                    for district in rdlp.children:
                        if int(district.district_id) == int(district_id):
                            for forestry in district.children:
                                if int(forestry.forestry_id) == int(forestry_id):
                                    data = {}
                                    for i, element in enumerate(forestry.children):
                                        data[i] = element.json

                                    return jsonify(data)

            return jsonify({"status": "error"})

        @self.app.route('/display_sector/<address>')
        def display_sector(address: str):
            rdlp_id = int(address.split("-")[0])
            district_id = int(address.split("-")[1])
            forestry_id = int(address.split("-")[2])
            for rdlp in self.forest.rdlp_data.values():
                if rdlp.id == rdlp_id:
                    name = self.forest.normalize_rdlp_name(rdlp.name)
                    sectors = self.forest.sectors_data[name]
                    for sector in sectors:
                        if sector.address == address:
                            data = sector.json
                            data["rdlp"] = rdlp.name
                            data["district"] = self.forest.district_data[f"{rdlp_id}-{district_id}"]
                            #data["forestry"] = self.forest.district_data[f"{rdlp_id}-{district_id}-{forestry_id}"]
                            return data

            return jsonify({"status": "error"})