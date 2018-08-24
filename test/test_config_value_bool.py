# coding=utf-8

import pathlib

import pytest

# noinspection PyProtectedMember
import elib_config._value._exc
# noinspection PyProtectedMember
from elib_config._value import _config_value_bool


@pytest.fixture(name='value')
def _dummy_string_value():
    yield _config_value_bool.ConfigValueBool(
        'key',
        description='desc',
        default=True,
    )


def test_no_default():
    value = _config_value_bool.ConfigValueBool(
        'test', 'value',
        description='test',
    )
    with pytest.raises(elib_config._value._exc.ConfigMissingValueError):
        value()


def test_string_value_default(value):
    assert value() is True


def test_string_value_type_name(value):
    assert value.type_name == 'boolean'


@pytest.mark.parametrize(
    'file_value',
    [
        10,
        '"true"',
        '["some", "list"]',
        '{some = "dict"}',
    ]
)
def test_invalid_cast_type_from_config_file(value, file_value):
    pathlib.Path('config.toml').write_text(f'key = {file_value}')
    exc_msg = f'{value.name}: invalid boolean expression: ".*"; ' \
              f'use either "true" or "false" instead, without the quotes.'
    with pytest.raises(elib_config._value._exc.ConfigTypeError, match=exc_msg):
        value()


def test_valid_cast_type_from_config_file(value):
    pathlib.Path('config.toml').write_text(f'key = false')
    assert value() is False
