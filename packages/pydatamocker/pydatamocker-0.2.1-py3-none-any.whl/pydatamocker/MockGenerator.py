from pandas import DataFrame
from .io import write_dataframe, load_json, write_json, load_table
from .builder import build_dataframe
from .util.list import dedup_list, list_diff


def _config_column_order(specified, fields_dict):
    if not specified or len(specified) < 1:
        return fields_dict
    spec_dedup = dedup_list(specified)
    order = spec_dedup + list_diff(fields_dict.keys(), spec_dedup)
    return { key: fields_dict[key] for key in order }


class MockGenerator:

    dataframe: DataFrame
    fields_describe = {
        'fields': dict()
    }

    def __init__(self, config = None) -> None:
        if config:
            self.fields_describe = load_json(config)

    def dump_config(self, path, pretty=True, indent=2):
        write_json(self.fields_describe, path, pretty, indent)

    def add_field(self, name: str, mock_type:str, **props):
        self.fields_describe['fields'][name] = {
            'mock_type': mock_type,
            'props': props
        }

    def add_fields(self, fields_dict: dict):
        self.fields_describe['fields'].update(fields_dict)

    def add_table(self, path: str):
        columns = load_table(path).columns
        for col in columns:
            self.fields_describe['fields'][col] = {'mock_type': 'table', 'props': { 'path': path }}

    def sample(self, size: int):
        self.dataframe = build_dataframe(self.fields_describe, size)

    def get_dataframe(self):
        return self.dataframe.copy()

    def dump(self, path):
        if not path:
            raise ValueError('Path must be specified')
        write_dataframe(path, self.dataframe)

    def set_column_order(self, order):
        self.fields_describe['fields'] = _config_column_order(order, self.fields_describe['fields'])

    def __str__(self) -> str:
        self.dataframe.__str__()

    def __repr__(self) -> str:
        self.dataframe.__str__()
