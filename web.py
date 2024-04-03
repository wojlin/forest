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
            for i, element in enumerate(self.forest.rdlp_data):
                data[i] = element.json()
            return jsonify(data)

        @self.app.route('/get_district')
        def get_district():
            data = {}
            for i, element in enumerate(self.forest.district_data):
                data[i] = element.json()
            return jsonify(data)

        @self.app.route('/get_forestry')
        def get_forestry():
            data = {}
            for i, element in enumerate(self.forest.forestry_data):
                data[i] = element.json()
            return jsonify(data)