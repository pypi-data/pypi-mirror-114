from .io import load_dataset, load_table, DATASETS
from pandas import Series
from .numbers import get_sample as num_sample, TYPES as NUMTYPES
from .time import get_sample as time_sample


def _table_column_sample(path: str, field_name: str):
    dataset = load_table(path)
    return lambda size: [dataset[field_name].sample(n=size, replace=True).reset_index(drop=True)]


def get_sample_generators(field_name: str, mock_type: str, **props):
    if mock_type in DATASETS:
        return lambda size: load_dataset(mock_type).sample(n=size, ignore_index=True, replace=True)
    elif mock_type in NUMTYPES:
        return lambda size: num_sample(mock_type, size, **props)
    elif mock_type == 'enum':
        return lambda size: Series(props['values']).sample(n=size, ignore_index=True, replace=True, weights=props['weights'])
    elif mock_type in { 'date', 'datetime' }:
        return lambda size: time_sample(mock_type, size, **props)
    elif mock_type == 'table':
        return _table_column_sample(props['path'], field_name)
    else:
        raise ValueError('Unsupported type')
