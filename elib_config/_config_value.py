# coding=utf-8
"""
Defines config values as instances of ConfigValue that can be called to obtain their values.

Values will be looked for in the OS environment first, then in the config file. If no value is found, the default will
be returned, or an exception will be raised.

Config value have strong type that will be checked and enforced at runtime.

They also have a description, which will be used to create the example config file.
"""
import abc
import os
import typing

# noinspection PyProtectedMember
from elib_config._config_file import read_config_file
# noinspection PyProtectedMember
from elib_config._exc import ConfigMissingValueError, ConfigTypeError
# noinspection PyProtectedMember
from elib_config._setup import ELIBConfig
# noinspection PyProtectedMember
from elib_config._utils import friendly_type_name

SENTINEL = object()


class ConfigValue(abc.ABC):
    """
    Abstract base class for config values
    """
    config_values: typing.Dict[str, 'ConfigValue'] = {}

    def __init__(self, *path: str, description: str, default=SENTINEL) -> None:
        self.path: str = ELIBConfig.config_sep_str.join(path)
        self.default: object = default
        self.description: str = description
        ConfigValue.config_values[self.path] = self

    @property
    def name(self) -> str:
        """
        :return: user friendly name of this value as a string
        """
        return self.path.replace('__', ': ')

    def _from_environ(self) -> typing.Optional[object]:
        var_name = ELIBConfig.config_sep_str.join((ELIBConfig.app_name, self.path)).upper()
        for env_var in os.environ:
            if env_var.upper() == var_name:
                return os.getenv(env_var)
        return None

    def _from_config_file(self) -> typing.Optional[object]:
        value = read_config_file()
        for key in self.path.split(ELIBConfig.config_sep_str):
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
        """
        :return: raw value
        """
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
        actual_type: str = friendly_type_name(type(self.raw_value()))
        raise ConfigTypeError(
            self.path,
            f'config value must be of type "{self.type_name}", got "{actual_type}" instead.'
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
