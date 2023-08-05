from pandas import Series, DataFrame, concat
from .sampler import get_sample_generators
from .config import get_configs

# def build_series(name: str, field_descriptor: dict, size: int):
    # get_sample = get_sample_generators(field_descriptor['mock_type'], **field_descriptor['props'])
    # return Series(data=get_sample(size), name=name)


def build_dataframe(fields_describe: dict, size: int) -> DataFrame:
    df = None
    report_progress = get_configs('report_progress')
    for field, field_spec in fields_describe['fields'].items():
        report_progress and print('Sampling', field, '...')
        sample = get_sample_generators(field, field_spec['mock_type'], **field_spec['props'])(size)
        if not type(sample) is Series:
            name = field
        else:
            name = sample.name or field
        df = concat([df, Series(sample, name=name)], axis=1)
    report_progress and print('Done!')
    return df
