# coding=utf-8
"""
Config value that will be cast as a string
"""
import typing

import dataclasses
import tomlkit.container

from ._config_value import ConfigValue, SENTINEL
from ._exc import MissingTableKeyError, TableKeyTypeError
from elib_config._utils import friendly_type_name


@dataclasses.dataclass
class ConfigValueTableKey:
    """
    Represents a value in the table
    """
    key_name: str
    key_type: typing.Type
    description: str
    default: typing.Any = SENTINEL  # noqa

    @property
    def user_friendly_type(self) -> str:
        """
        :return: user friendly type of the key
        :rtype: str
        """
        return friendly_type_name(self.key_type)

    @property
    def mandatory(self) -> bool:
        """
        :return: True if this key has no default
        :rtype: bool
        """
        return self.default is SENTINEL


class ConfigValueTableArray(ConfigValue):
    """
    Config value that will be cast as a string
    """

    def __init__(self,
                 *path: str,
                 description: str,
                 default=SENTINEL,
                 keys: typing.Iterable[ConfigValueTableKey] = SENTINEL) -> None:
        super(ConfigValueTableArray, self).__init__(*path, description=description, default=default)
        self.keys = [] if keys is SENTINEL else keys

    @property
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return 'array of tables'

    def _check_keys(self, raw_value: dict) -> dict:
        for key in self.keys:
            if key.key_name not in raw_value:
                if key.mandatory:
                    raise MissingTableKeyError(self.name, str(key))
                else:
                    key_value = key.default
                    raw_value[key.key_name] = key_value
            else:
                key_value = raw_value[key.key_name]
            if not isinstance(key_value, key.key_type):
                raise TableKeyTypeError(self.name,
                                        key.key_name,
                                        friendly_type_name(key.key_type),
                                        friendly_type_name(type(key_value)),
                                        )
        return raw_value

    def _cast(self, raw_value) -> dict:
        if not isinstance(raw_value, dict):
            self._raise_invalid_type_error()
        raw_value_as_dict = self._check_keys(dict(raw_value))
        return raw_value_as_dict

    # pylint: disable=useless-super-delegation
    def __call__(self) -> dict:
        return super(ConfigValueTableArray, self).__call__()

    def __getattr__(self, item):
        if item in (key.key_name for key in self.keys):
            return self()[item]

        raise AttributeError(f'{self.name}: table has no key "{item}"')

    def __getitem__(self, item):
        return self.__getattr__(item)

    def _toml_add_value_type(self, toml_obj: tomlkit.container.Container):
        self._toml_comment(toml_obj, f'value type: {self.friendly_type_name}')
        self._toml_comment(toml_obj, '')
        self._toml_comment(toml_obj, 'Type of keys:')
        for key in self.keys:
            if key.mandatory:
                _key_state = 'This key is MANDATORY'
            else:
                _key_state = 'This key is optional, and has a default value of: ' + str(key.default)
            _comments = [
                f'key name: {key.key_name}',
                f'key type: {key.user_friendly_type}',
                key.description,
                _key_state,
                '',
            ]
            for comment in _comments:
                toml_obj.add(tomlkit.comment((' ' * 4 + comment).rstrip()))

    def _generate_example(self) -> typing.List[str]:
        _doc = tomlkit.document()
        _table = tomlkit.table()
        for key in self.keys:
            if not key.mandatory:
                _value = key.default
            else:
                if key.key_type == str:
                    _value = "some text"
                elif key.key_type == int:
                    _value = 1
                elif key.key_type == float:
                    _value = 1.0
                elif key.key_type == bool:
                    _value = True
                else:
                    raise KeyError(f'unmanaged key type: {key.key_type}')
            _table[key.key_name] = _value
        _array = tomlkit.aot()
        _array.append(_table)
        _doc[self.key] = _array
        return _doc.as_string().split('\n')

    def _toml_add_examples(self, toml_obj: tomlkit.container.Container):
        self._toml_comment(toml_obj, 'An array of tables is a list of table that share a common schema of '
                                     'key/value pairs.')
        self._toml_comment(toml_obj, r'example:')
        for line in self._generate_example():
            self._toml_comment(toml_obj, (' ' * 4 + line).rstrip())
        self._toml_comment(toml_obj, r'NOTE: the above example can be repeated as many times as needed, to create '
                                     r'multiple tables in the array.')

    def _toml_add_comments(self, toml_obj: tomlkit.container.Container):
        super(ConfigValueTableArray, self)._toml_add_comments(toml_obj)

    def _toml_add_value(self, toml_obj: tomlkit.container.Container, not_set: str):
        if self.default != SENTINEL:
            _doc = tomlkit.document()
            _doc[self.key] = self.default
            for line in _doc.as_string().split('\n'):
                self._toml_comment(toml_obj, line)
        else:
            toml_obj[self.key] = not_set
            toml_obj.add(tomlkit.nl())
