# coding=utf-8
"""
This package manages configuration for other packages.

It is intended for my personal use only
"""
import typing
from pathlib import Path

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution('elib_config').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'


class ELIBConfigSetup:
    config_file_path: typing.Optional[Path] = None
    sep_str: str = '__'
