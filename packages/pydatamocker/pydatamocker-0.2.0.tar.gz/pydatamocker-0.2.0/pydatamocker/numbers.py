import numpy as np
from .util.math import range_step
from .util.functions import compose

_distribution_samples = {
    'float': {
        'normal': compose(False,
                lambda **kw: np.random.normal(kw['mean'], kw['std'], kw['size'])
        ),
        'uniform': compose(False,
            lambda **kw: np.random.uniform(kw['min'], kw['max'], kw['size'])
        ),
        'range': compose(False,
            lambda **kw: np.arange(kw['start'], kw['end'], range_step(kw['start'], kw['end'], kw['size'])),
            lambda f: lambda **kw: f(**kw).astype(float)[:kw['size']]
        )
    },
    'integer': {
        'uniform': compose(False,
            lambda **kw: np.random.random_integers(kw['min'], kw['max'], kw['size'])
        ),
        'binomial': compose(False,
            lambda **kw: np.random.binomial(kw['n'], kw['p'], kw['size'])
        ),
        'range': compose(False,
            lambda **kw: np.arange(kw['start'], kw['end'], range_step(kw['start'], kw['end'], kw['size'])),
            lambda f: lambda **kw: f(**kw).astype(int)[:kw['size']]
        )
    }
}


TYPES = { 'float', 'integer' }


DISTRIBUTIONS = {
    'normal': { 'mean', 'std' },
    'uniform': { 'min', 'max' },
    'binomial' : { 'n', 'p' },
    'range': { 'start', 'end' }
}


def get_sample(dtype: str, size: int = None, **props):
    size = size or props['size']
    distr = props['distr']
    return _distribution_samples[dtype][distr]( **(props | {'size': size}) )
