import json
import os

from flask import Flask, send_file, request
import pandas as pd


app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), ''),
    static_url_path=''
    )

class DataService(object):

    dataframes = {}
    asset_paths = {
            'CO_WS_2011': {
                'path': 'data/CO_WS_2011_2012.txt',
                'sep': '\t'
                },
            'USGS_FAA': {
                'path': 'data/USGS_WindTurbine_201307_cleaned.csv',
                'sep': ','
                }
        }

    def __init__(self):
        """Read data into DataFrames"""
        for name, params in self.asset_paths.items():
            df = pd.read_table(params['path'], sep=params['sep'])
            self.dataframes[name] = df

    def __repr__(self):
        return "DataService"

    def get_dimensions(self, asset_name):
        """
        Get dimensions

        Parameters
        ----------
        asset_name: str

        Returns
        -------
        List of column names
        """
        df = self.dataframes[asset_name]
        return df.columns.tolist()


data_service = DataService()

@app.route('/')
def index():
    """Serve index.html"""
    return send_file('index.html')


@app.route('/dimensions', methods=['POST'])
def dimensions():
    """Given the name of an asset, return column names (dimensions)"""
    req = json.loads(request.data)
    dimensions = data_service.get_dimensions(req['name'])
    return json.dumps(dimensions)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
