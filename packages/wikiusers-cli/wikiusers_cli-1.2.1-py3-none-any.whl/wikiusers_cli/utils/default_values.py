import os
from pathlib import Path
from wikiusers import settings

_prefix = 'WIKIUSERS_'


def _get_value_str(name: str, default_value: str) -> str:
    env_value = os.environ.get(name)
    return default_value if env_value is None else env_value


def _get_value_int(name: str, default_value: int) -> int:
    try:
        return int(os.environ[name])
    except:
        return default_value


def _get_value_bool(name: str, default_value: bool) -> bool:
    env_value = os.environ.get(name)
    if env_value in ['FALSE', 'False', 'false', '0']:
        return False
    if env_value in ['TRUE', 'True', 'true', '1']:
        return True
    return default_value


def _get_value_path(name: str, default_value: str) -> Path:
    env_value = os.environ.get(name)
    return default_value if env_value is None else Path(env_value)


def _get_value(name: str, default_value, value_type: str):
    env_name = _prefix + name
    if value_type == 'str':
        return _get_value_str(env_name, default_value)
    if value_type == 'int':
        return _get_value_int(env_name, default_value)
    if value_type == 'bool':
        return _get_value_bool(env_name, default_value)
    if value_type == 'path':
        return _get_value_path(env_name, default_value)
    return default_value


_default_options_objects = [
    {
        'name': 'DATASETS_DIR',
        'default_value': settings.DEFAULT_DATASETS_DIR,
        'value_type': 'path'
    },
    {
        'name': 'DATABASE_PREFIX',
        'default_value': settings.DEFAULT_DATABASE_PREFIX,
        'value_type': 'str'
    },
    {
        'name': 'LANGUAGE',
        'default_value': settings.DEFAULT_LANGUAGE,
        'value_type': 'str'
    },
    {
        'name': 'SYNC_DATA',
        'default_value': settings.DEFAULT_SYNC_DATA,
        'value_type': 'bool'
    },
    {
        'name': 'PARALLELIZE',
        'default_value': settings.DEFAULT_PARALLELIZE,
        'value_type': 'bool'
    },
    {
        'name': 'N_PROCESSES',
        'default_value': settings.DEFAULT_N_PROCESSES,
        'value_type': 'int'
    },
    {
        'name': 'BATCH_SIZE',
        'default_value': settings.DEFAULT_BATCH_SIZE,
        'value_type': 'int'
    },
    {
        'name': 'FORCE',
        'default_value': settings.DEFAULT_FORCE,
        'value_type': 'bool'
    }, {
        'name': 'SKIP',
        'default_value': settings.DEFAULT_SKIP,
        'value_type': 'bool'
    },
    {
        'name': 'ERASE_DATASETS',
        'default_value': settings.DEFAULT_ERASE_DATASETS,
        'value_type': 'bool'
    },
]


DEFAULT_ARGUMENTS = {obj['name']: _get_value(
    **obj) for obj in _default_options_objects}
