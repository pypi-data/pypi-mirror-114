mocker_config = {}


def config(**kwargs):
    mocker_config.update(kwargs)


def get_configs(*keys):
    if len(list(keys)) == 0:
        keys = mocker_config.keys()
    return (config.get(key) for key in keys)
