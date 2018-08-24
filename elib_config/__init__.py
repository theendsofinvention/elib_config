# coding=utf-8
"""
This package manages configuration for other packages.

It is intended for my personal use only
"""

from pkg_resources import DistributionNotFound, get_distribution

# noinspection PyUnresolvedReferences
from ._setup import ELIBConfig

try:
    __version__ = get_distribution('elib_config').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'
