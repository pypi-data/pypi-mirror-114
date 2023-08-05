import os.path as osp
from pandas import read_pickle, read_csv, DataFrame
from pathlib import Path
import json


class _Datacache:

    data = {}

    def __init__(self):
        return

    def write(self, key: str, data, **kwargs):
        self.data[key] = { 'data': data }
        self.data[key].update(kwargs)

    def read(self, key: str):
        if not self.data.get(key):
            return None
        return self.data[key]['data']

    def get_props(self, key: str, *props):
        return { key: self.data[key][kw] for kw in props }


_cache = _Datacache()


_df_writers = {
    '.pkl' : lambda file, dataframe: dataframe.to_pickle(file, index=True),
    '.csv' : lambda file, dataframe: dataframe.to_csv(file, index=False),
    '.tsv' : lambda file, dataframe: dataframe.to_csv(file, sep="\t", index=False),
    '.json' : lambda file, dataframe: dataframe.to_json(file, orient='table', index=False)
}


get_dataset_path = lambda dataset: osp.join(osp.dirname(__file__), osp.pardir, 'data', dataset + '.pkl')


DATASETS = { 'first_name', 'last_name' }


def load_dataset(dataset: str):
    path = get_dataset_path(dataset)
    data = _cache.read(path)
    if data is None:
        data = read_pickle(path)
        _cache.write(path, data)
    return data


def load_table(path: str):
    data = _cache.read(path)
    if data is None:
        data = read_csv(path)
        _cache.write(path, data)
    return data


def write_dataframe(file: str, dataframe: DataFrame):
    file_ext = Path(file).suffix
    if file_ext is None or not file_ext in _df_writers.keys():
        file_ext = '.csv'
    _df_writers[file_ext](file, dataframe)


def load_json(file) -> dict:
    f = open(file, 'rt') if type(file) is str else file
    return json.load(f)


def write_json(obj: dict, path: str, pretty: str, indent: int):
    with open(path, 'wt', ) as f:
        json.dump(obj, f, indent=(indent if pretty else None))
