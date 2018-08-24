# coding=utf-8

import os
import pathlib

import pytest

# noinspection PyProtectedMember
import elib_config._value._exc
# noinspection PyProtectedMember
from elib_config._value import _config_value


@pytest.fixture(name='dummy_value')
def _dummy_value():
    dummy_value = DummyConfigValue(
        'dummy', 'test', 'config_value',
        description='test description'
    )
    yield dummy_value


class DummyConfigValue(_config_value.ConfigValue):

    def _cast(self, raw_value):
        return raw_value

    @property
    def type_name(self) -> str:
        return 'test'


def test_config_value_basic(dummy_value):
    assert isinstance(dummy_value, _config_value.ConfigValue)
    dummy_value.default = 'some default'
    assert dummy_value() == 'some default'
    assert dummy_value.type_name == 'test'
    assert dummy_value.name == 'dummy: test: config_value'


def test_value_no_default(dummy_value):
    with pytest.raises(elib_config._value._exc.ConfigMissingValueError):
        dummy_value()


def test_value_in_environ(dummy_value):
    with pytest.raises(elib_config._value._exc.ConfigMissingValueError):
        dummy_value()
    os.environ['TEST__DUMMY__TEST__CONFIG_VALUE'] = 'test_value'
    assert dummy_value() == 'test_value'
    del os.environ['TEST__DUMMY__TEST__CONFIG_VALUE']


def test_value_in_config_file(dummy_value):
    pathlib.Path('config.toml').write_text(
        """
        [dummy.test]
        config_value = "some value"
        """
    )
    assert dummy_value() == 'some value'
