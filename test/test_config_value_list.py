# coding=utf-8

import pathlib

import pytest

# noinspection PyProtectedMember
from elib_config import _config_value_list, _exc, _utils


@pytest.fixture(name='value')
def _dummy_string_value():
    yield _config_value_list.ConfigValueList(
        'key',
        element_type=str,
        description='desc',
        default=['some', 'list'],
    )


def test_no_default():
    value = _config_value_list.ConfigValueList(
        'test', 'value',
        element_type=str,
        description='test',
    )
    with pytest.raises(_exc.ConfigMissingValueError):
        value()


def test_string_value_default(value: _config_value_list.ConfigValueList):
    assert value() == ['some', 'list']


def test_string_value_type_name(value: _config_value_list.ConfigValueList):
    assert value.type_name == 'List of strings'


@pytest.mark.parametrize(
    'file_value,wrong_type',
    [
        (10, "integer"),
        (10.01, "float"),
        ('"some string"', 'string'),
        ('true', 'boolean'),
        ('{some = "dict"}', 'dictionary'),
    ]
)
def test_invalid_cast_type_from_config_file(value: _config_value_list.ConfigValueList, file_value, wrong_type):
    pathlib.Path('config.toml').write_text(f'key = {file_value}')
    exc_msg = f'{value.name}: config value must be of type "List of strings", got "{wrong_type}" instead'
    with pytest.raises(_exc.ConfigTypeError, match=exc_msg):
        value()


def test_valid_cast_type_from_config_file(value: _config_value_list.ConfigValueList):
    pathlib.Path('config.toml').write_text(f'key = ["some", "other", "list"]')
    assert value() == ['some', 'other', 'list']


@pytest.mark.parametrize(
    'not_a_string',
    (True, False, 10, 10.05, ['another', 'list'], {'a': 'dict'})
)
def test_element_type_check(value: _config_value_list.ConfigValueList, not_a_string):
    value.default = ['string', 'string_too', not_a_string]
    actual_type = _utils.friendly_type_name(type(not_a_string))
    error = f'{value.name}: item at index 2 should be a "string", but is "{actual_type}" instead'
    with pytest.raises(_config_value_list.ConfigTypeError, match=error):
        value()


@pytest.mark.parametrize(
    'not_a_string',
    ('true', 'false', '10', '10.05', '["another", "list"]', '{a = "dict"}')
)
def test_element_type_check_from_file(value: _config_value_list.ConfigValueList, not_a_string):
    pathlib.Path('config.toml').write_text(f'key = [ {not_a_string} ]')
    error = f'{value.name}: item at index 0 should be a "string", but is .* instead'
    with pytest.raises(_config_value_list.ConfigTypeError, match=error):
        value()
