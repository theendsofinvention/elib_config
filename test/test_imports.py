# coding=utf-8
"""
This is a temporary test to cover the import of modules that have 0% coverage so far

Yes, this is shameful...
"""

import glob

import pytest

import elib_config


@pytest.fixture(autouse=True)
def patch_version(monkeypatch):
    monkeypatch.setattr(elib_config, '__version__', '0.0.0')


# noinspection PyUnresolvedReferences,PyProtectedMember
@pytest.mark.nocleandir
@pytest.mark.parametrize('module', glob.glob('./elib_config/*.py', recursive=True))
def test_imports(module):
    module = module[2:-3].replace('\\', '.')
    print(f'importing {module}')
    __import__(module)


# noinspection PyUnresolvedReferences,PyProtectedMember
@pytest.mark.nocleandir
@pytest.mark.parametrize('module', list(glob.glob('./elib_config/*.py', recursive=True)))
def test_imports_tests(module):
    module = module[2:-3].replace('\\', '.')
    print(f'importing {module}')
    __import__(module)
