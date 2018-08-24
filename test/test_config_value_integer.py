# coding=utf-8

import pathlib

import pytest

# noinspection PyProtectedMember
import elib_config._value._exc
# noinspection PyProtectedMember
from elib_config._value import _config_value_integer


@pytest.fixture(name='value')
def _dummy_string_value():
    yield _config_value_integer.ConfigValueInteger(
        'key',
        description='desc',
        default=10,
    )


def test_no_default():
    value = _config_value_integer.ConfigValueInteger(
        'test', 'value',
        description='test',
    )
    with pytest.raises(elib_config._value._exc.ConfigMissingValueError):
        value()


def test_string_value_default(value):
    assert value() is 10


def test_string_value_type_name(value):
    assert value.type_name == 'integer'


@pytest.mark.parametrize(
    'file_value',
    [
        '"string"',
        '"10"',
        'true',
        '["some", "list"]',
        '{some = "dict"}',
    ]
)
def test_invalid_cast_type_from_config_file(value, file_value):
    pathlib.Path('config.toml').write_text(f'key = {file_value}')
    exc_msg = f'{value.name}: config value must be of type "integer", got .* instead'
    with pytest.raises(elib_config._value._exc.ConfigTypeError, match=exc_msg):
        value()


def test_valid_cast_type_from_config_file(value):
    pathlib.Path('config.toml').write_text(f'key = 5')
    assert value() is 5


def test_min(value: _config_value_integer.ConfigValueInteger):
    assert value() is 10
    value.set_limits(min_=10)
    assert value() is 10
    value.set_limits(min_=11)
    with pytest.raises(_config_value_integer.OutOfBoundError):
        value()


def test_max(value: _config_value_integer.ConfigValueInteger):
    assert value() is 10
    value.set_limits(max_=10)
    assert value() is 10
    value.set_limits(max_=9)
    with pytest.raises(_config_value_integer.OutOfBoundError):
        value()


def test_min_max(value: _config_value_integer.ConfigValueInteger):
    assert value() is 10
    value.set_limits(min_=10, max_=10)
    assert value() is 10
    value.set_limits(max_=9)
    with pytest.raises(_config_value_integer.OutOfBoundError):
        value()
    value.set_limits(min_=11, max_=11)
    with pytest.raises(_config_value_integer.OutOfBoundError):
        value()
