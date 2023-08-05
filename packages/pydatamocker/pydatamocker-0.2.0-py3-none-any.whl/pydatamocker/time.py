import pandas as pd
from numpy import arange
from .util.functions import compose


ISO_DATETIME = '%Y-%m-%dT%H:%M%:%SZ'

ISO_DATE = '%Y-%m-%d'


default_format = {
    'date': ISO_DATE,
    'datetime': ISO_DATETIME
}


_distribution_samples = {
    'range': compose(False,
        lambda **kw: pd.date_range(start=kw['start'], end=kw['end'], periods=kw['size']),
        lambda f: lambda **kw: f(**kw).strftime(default_format[kw['type']]),
        lambda f: lambda **kw: f(**kw).to_series(index=arange(kw['size']))
    ),
}
_distribution_samples['uniform'] = (
    compose(False,
        lambda **kw: pd.date_range(_distribution_samples['range'])(**kw),
        lambda f: lambda **kw: f(**kw).sample(frac=1).reset_index(drop=True)
    )
)


def get_sample(mock_type: str, size: int, **kw):
    kw['type'] = mock_type
    distr = kw['distr']
    return _distribution_samples[distr](**( kw | {'size' : size} ) )
