# coding=utf-8
"""
Reads and writes ESST's config to/from a file.
"""
import multiprocessing
import sys
from pathlib import Path

import toml

from ._exc import ConfigFileNotFoundError
from ._setup import ELIBConfig

CONFIG_LOCK = multiprocessing.Lock()
""":py:class:`multiprocessing.Lock` that blocks concurrent access to the config file by multiple processes"""


def _ensure_config_file_exists():
    """
    Makes sure the config file exists.

    :raises: :class:`epab.core.new_config.exc.ConfigFileNotFoundError`
    """
    config_file = Path(ELIBConfig.config_file_path).absolute()
    if not config_file.exists() and not getattr(sys, '_called_from_test'):
        raise ConfigFileNotFoundError(config_file)


def _read_file() -> dict:
    config_file = Path(ELIBConfig.config_file_path).absolute()
    if not config_file.exists():
        return {}
    with config_file.open(encoding='utf8') as stream:
        try:
            return toml.load(stream)
        except toml.TomlDecodeError:
            raise ValueError('invalid config file')


def _write_file(config: dict):
    config_file = Path(CONFIG_FILE_PATH).absolute()
    with config_file.open(mode='w', encoding='utf8') as stream:
        yaml.dump(config, stream, Dumper=yaml.RoundTripDumper)


def read_config_file(package: str = None) -> dict:
    """
    Reads configuration from the disk.

    :param str package: optional package; if ``None``, reads the whole config.
    :return: configuration dictionary.
    :raises MissingConfigPackageError: raised if ``package`` is not ``None`` and it doesn't exist at the top level of
        the config file.
    """
    config = _read_file()
    if package is None:

        return config
    else:
        try:
            return config[package]
        except KeyError:
            raise MissingConfigPackageError(f'missing module in configuration file: {package}')
