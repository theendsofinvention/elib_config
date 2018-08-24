# coding=utf-8

import pathlib

import pytest

# noinspection PyProtectedMember
from elib_config import _exc
from elib_config._value import _config_value_path


@pytest.fixture(name='value')
def _dummy_string_value():
    yield _config_value_path.ConfigValuePath(
        'key',
        description='desc',
        default='some path',
    )


def test_no_default():
    value = _config_value_path.ConfigValuePath(
        'test', 'value',
        description='test',
    )
    with pytest.raises(_exc.ConfigMissingValueError):
        value()


def test_string_value_default(value):
    assert value() == pathlib.Path('some path').absolute()


def test_string_value_type_name(value):
    assert value.type_name == 'path'


@pytest.mark.parametrize(
    'file_value',
    [
        10,
        'true',
        '["some", "list"]',
        '{some = "dict"}',
    ]
)
def test_invalid_cast_type_from_config_file(value, file_value):
    pathlib.Path('config.toml').write_text(f'key = {file_value}')
    exc_msg = f'{value.name}: config value must be of type "path", got .* instead'
    with pytest.raises(_exc.ConfigTypeError, match=exc_msg):
        value()


def test_valid_cast_type_from_config_file(value):
    pathlib.Path('config.toml').write_text(f'key = "some other path"')
    assert value() == pathlib.Path('some other path').absolute()


def test_path_value_file(value):
    test_file = pathlib.Path('some path').absolute()
    assert not test_file.exists()
    test_value = value()
    test_value.touch()
    assert test_file.exists()


def test_path_value_must_exist(value: _config_value_path.ConfigValuePath):
    value.must_exist()
    test_file = pathlib.Path('some path').absolute()
    assert not test_file.exists()
    with pytest.raises(_exc.PathMustExistError):
        value()
    test_file.touch()
    value()


def test_path_value_must_be_file_with_file(value: _config_value_path.ConfigValuePath):
    value.must_be_file()
    test_path = pathlib.Path('some path')
    test_path.touch()
    value()


def test_path_value_must_be_file_with_dir(value: _config_value_path.ConfigValuePath):
    value.must_be_file()
    test_path = pathlib.Path('some path')
    test_path.mkdir()
    with pytest.raises(_exc.NotAFileError):
        value()
    test_path.rmdir()
    value.must_exist()
    with pytest.raises(_exc.PathMustExistError):
        value()


def test_path_value_must_be_dir_with_dir(value: _config_value_path.ConfigValuePath):
    value.must_be_dir()
    test_path = pathlib.Path('some path')
    test_path.mkdir()
    value()


def test_path_value_must_be_dir_with_file(value: _config_value_path.ConfigValuePath):
    value.must_be_dir()
    test_path = pathlib.Path('some path')
    test_path.touch()
    with pytest.raises(_exc.NotAFolderError):
        value()
    test_path.unlink()
    value.must_exist()
    with pytest.raises(_exc.PathMustExistError):
        value()


def test_path_value_create_missing_dir(value: _config_value_path.ConfigValuePath):
    test_path = pathlib.Path('some path')
    value.create_dir()
    assert not test_path.exists()
    value()
    assert test_path.exists()
