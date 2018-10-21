# coding=utf-8
"""
This module is responsible for writing an example config file in case it is missing or incorrect
"""
import textwrap
import typing

import uuid
import tomlkit
from tomlkit.container import Container as TOMLContainer

from collections import defaultdict


from elib_config._types import Types
# noinspection PyProtectedMember
from elib_config._value._config_value_table import ConfigValueTableArray
from elib_config._setup import ELIBConfig
# noinspection PyProtectedMember
from elib_config._value._config_value import ConfigValue, SENTINEL
from elib_config._file._config_example_header import HEADER


_NOT_SET = uuid.uuid4().hex


def _nested_default_dict() -> defaultdict:
    return defaultdict(_nested_default_dict)


def default_dict_to_dict(source) -> dict:
    for k, v in source.items():
        if isinstance(v, dict):
            source[k] = default_dict_to_dict(v)
    return dict(source)


def _get_header() -> typing.List[str]:
    return HEADER.format(
        app_version=ELIBConfig.app_version,
        app_name=ELIBConfig.app_name,
        config_file_path=ELIBConfig.config_file_path,
        sep=ELIBConfig.config_sep_str,
    ).split('\n') + ['', 'START OF ACTUAL CONFIG FILE']


def _aggregate_config_values(config_values: typing.List[ConfigValue]) -> dict:
    """
    Returns a (sorted)

    :param config_values:
    :type config_values:
    :return:
    :rtype:
    """
    _keys: defaultdict = _nested_default_dict()
    _sorted_values = sorted(config_values, key=lambda x: x.name)
    for value in _sorted_values:
        value_keys = value.path.split(ELIBConfig.config_sep_str)
        this_config_key = _keys
        for sub_key in value_keys[:-1]:
            this_config_key = this_config_key[sub_key]
        this_config_key[value_keys[-1]] = value
    return default_dict_to_dict(_keys)


def _add_config_values_to_toml_object(toml_obj: TOMLContainer, data: typing.Dict[str, typing.Union[dict, ConfigValue]]):
    if isinstance(data, dict):
        for key_name, key_data in data.items():
            if isinstance(key_data, dict):
                table = tomlkit.table()
                _add_config_values_to_toml_object(table, key_data)
                toml_obj[key_name] = table
            else:
                key_data.add_to_toml_obj(toml_obj, _NOT_SET)
                # _add_value_to_container(toml_obj, key_data)


def write_example_config(example_file_path: str):
    """
    Writes an example config file using the config values declared so far

    :param example_file_path: path to write to
    """
    document = tomlkit.document()
    _hdr = _get_header()
    for header_line in _get_header():
        document.add(tomlkit.comment(header_line))
    config_keys = _aggregate_config_values(ConfigValue.config_values)
    _add_config_values_to_toml_object(document, config_keys)
    _doc_as_str = document.as_string().replace(f'"{_NOT_SET}"', '')
    with open(example_file_path, 'w') as stream:
        stream.write(_doc_as_str)


if __name__ == '__main__':
    import elib_config
    elib_config.ELIBConfig.setup(
        app_version='version',
        app_name='app_name',
        config_file_path='test.toml',
        config_sep_str='__',
    )
    elib_config.ConfigValueString(
        'some', 'nested1', 'string',
        description='desc',
        default='test',
    )
    elib_config.ConfigValueBool(
        'some', 'nested1', 'bool',
        description='desc',
        default=True,
    )
    elib_config.ConfigValueInteger(
        'some', 'nested1', 'integer',
        description='desc',
        default=1,
    )
    elib_config.ConfigValueFloat(
        'some', 'nested2', 'float',
        description='desc',
        default=1.0,
    )
    elib_config.ConfigValueList(
        'some', 'nested2', 'list_of_string',
        description='desc',
        default=['some', 'list', 'of', 'strings'],
        element_type=str,
    )
    elib_config.ConfigValueList(
        'some', 'nested2', 'list_of_integers',
        description='desc',
        default=[1, 2, 3, 4],
        element_type=int,
    )
    elib_config.ConfigValueTableArray(
        'some', 'table_of_arrays',
        description='desc',
        keys=(elib_config.ConfigValueTableKey(key_name='key1',
                                              description='key description',
                                              key_type=str,
                                              # default='test',
                                              ),
              elib_config.ConfigValueTableKey(key_name='key2',
                                              description='key description',
                                              key_type=int,
                                              # default=1,
                                              )
              ),
        # default=[{'key': 'value'}, {'key': 'value'}],
        default=[],
    )
    elib_config.ConfigValueString(
        'some', 'nested3', 'string',
        description='desc',
    ),
    elib_config.ConfigValuePath(
        'some', 'nested4', 'path',
        description='desc',
        must_exist=True, must_be_file=True,
    )
    elib_config.ConfigValuePath(
        'some', 'nested4', 'path2',
        description='desc',
        must_exist=True, must_be_dir=True,
    )
    write_example_config('test.toml')

