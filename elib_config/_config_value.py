# coding=utf-8
import abc
import os
import typing
from pathlib import Path

from elib_config import ELIBConfigSetup
from ._config_file import read_config_file
from ._exc import ConfigMissingValueError, ConfigTypeError, NotAFileError, NotAFolderError, PathMustExistError

SENTINEL = object()


class ConfigValue(abc.ABC):
    config_values: typing.Dict[str, 'ConfigValue'] = {}

    def __init__(self, *path: str, description: str, default=SENTINEL):
        self.path: str = ELIBConfigSetup.sep_str.join(path)
        self.default: object = default
        self.description: str = description
        ConfigValue.config_values[self.path] = self

    @property
    def name(self) -> str:
        return self.path.replace('__', ': ')

    def _from_environ(self) -> typing.Optional[object]:
        var_name = ELIBConfigSetup.sep_str.join(('ESST', self.path)).upper()
        for env_var in os.environ:
            if env_var.upper() == var_name:
                return os.getenv(env_var)
        return None

    def _from_config_file(self) -> typing.Optional[object]:
        value = read_config_file()
        for key in self.path.split(ELIBConfigSetup.sep_str):
            try:
                value = value[key]
            except KeyError:
                return None

        return value

    def _from_default(self) -> typing.Optional[object]:
        if self.default != SENTINEL:
            return self.default

        return None

    def raw_value(self) -> typing.Optional[object]:
        raw_value = self._from_environ()
        if raw_value is None:
            raw_value = self._from_config_file()
        if raw_value is None:
            raw_value = self._from_default()
        return raw_value

    def __call__(self):
        raw_value = self.raw_value()
        if raw_value is None:
            raise ConfigMissingValueError(self.path, 'missing config value')
        return self._cast(raw_value)

    def _raise_invalid_type_error(self):
        raise ConfigTypeError(
            self.path,
            f'config value must be of type "{self.type_name}", got {type(self.raw_value())} instead.'
        )

    @abc.abstractmethod
    def _cast(self, raw_value):
        pass

    @property
    @abc.abstractmethod
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        # if self.value_type is str:
        #     return 'string'
        # elif self.value_type is dict:
        #     return 'dictionary'
        # elif self.value_type is int:
        #     return 'integer'
        # elif self.value_type is float:
        #     return 'float'
        # elif self.value_type is bool:
        #     return 'boolean'
        # elif self.value_type is list:
        #     return 'list'


class ConfigValueString(ConfigValue):

    @property
    def type_name(self) -> str:
        return 'string'

    def _cast(self, raw_value) -> str:
        if not isinstance(raw_value, str):
            self._raise_invalid_type_error()
        return raw_value


class ConfigValueBool(ConfigValue):

    @property
    def type_name(self) -> str:
        return 'boolean'

    def _cast(self, raw_value) -> bool:
        if isinstance(raw_value, str):
            if raw_value.lower() == 'true':
                return True
            elif raw_value.lower() == 'false':
                return False
        raise ConfigTypeError(
            self.path,
            f'invalid boolean expression: "{raw_value}"; use either "true" or "false" instead.'
        )


class ConfigValuePath(ConfigValue):

    def __init__(self, *path: str, description: str, default=SENTINEL):
        ConfigValue.__init__(self, *path, description=description, default=default)
        self._must_be_file: bool = False
        self._must_be_dir: bool = False
        self._create_dir: bool = False
        self._must_exist: bool = False

    def must_exist(self):
        self._must_exist = True

    def must_be_file(self):
        self._must_be_file = True

    def must_be_dir(self):
        self._must_be_dir = True

    def create_dir(self):
        self._create_dir = True

    @property
    def type_name(self) -> str:
        return 'path'

    def _cast(self, raw_value) -> Path:
        path = Path(raw_value)
        if self._must_exist and not path.exists():
            raise PathMustExistError(self.path)
        if path.exists() and self._must_be_dir and not path.is_dir():
            raise NotAFolderError(self.path)
        if path.exists() and self._must_be_file and not path.is_file():
            raise NotAFileError(self.path)
        if not path.exists() and self._create_dir:
            path.mkdir(parents=True)
        return path.absolute()
