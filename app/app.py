import json
import os

from flask import Flask, send_file, request
import pandas as pd
import vincent


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
            if name == 'CO_WS_2011':
                df['Date & Time Stamp'] = pd.to_datetime(
                    df['Date & Time Stamp']
                    )
                df.index = df['Date & Time Stamp']
                df = df[:5000]
            self.dataframes[name] = df.dropna()

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


@app.route('/chart', methods=['POST'])
def get_chart():
    """Given a dataset, dims, and a chart type, return a chart spec"""
    req = json.loads(request.data)

    df = data_service.dataframes[req['dataset']]
    subset = df[[req['xdim'], req['ydim']]]

    chart_handler = getattr(vincent, req['chartType'])
    # Handle timestamps with the index
    if isinstance(df[req['xdim']][0], pd.Timestamp):
        chart = chart_handler(subset[req['ydim']], width=600, height=430)
    else:
        chart = chart_handler(subset, iter_idx=req['xdim'], width=600,
                              height=430)

    chart.axis_titles(x=req['xdim'], y=req['ydim'])

    spec = chart.to_json(pretty_print=False)
    return spec


if __name__ == "__main__":
    app.run(port=8000, debug=True)
