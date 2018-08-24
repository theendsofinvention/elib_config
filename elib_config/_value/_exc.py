# coding=utf-8
"""
Exceptions for the value package
"""
# noinspection PyProtectedMember
from elib_config._exc import ELIBConfigError


class _ConfigValueError(ELIBConfigError):
    """Base class for all config values errors"""

    def __init__(self, value_name: str, msg: str) -> None:
        self.value_name = value_name
        self.msg = msg
        super(_ConfigValueError, self).__init__(
            f'{value_name}: {msg}'
        )


class ConfigMissingValueError(_ConfigValueError):
    """Raised when a config value is missing"""


class ConfigValueError(_ConfigValueError):
    """Raised when a given value is invalid"""


class PathMustExistError(ConfigValueError):
    """Raised a file/folder is not present"""

    def __init__(self, value_name: str) -> None:
        super(PathMustExistError, self).__init__(
            value_name,
            'file/folder not found'
        )


class NotAFileError(ConfigValueError):
    """Raised when a given path is not a file"""

    def __init__(self, value_name: str) -> None:
        super(NotAFileError, self).__init__(
            value_name,
            'not a file'
        )


class NotAFolderError(ConfigValueError):
    """Raised when a given path is not a file"""

    def __init__(self, value_name: str) -> None:
        super(NotAFolderError, self).__init__(
            value_name,
            'not a folder'
        )


class ConfigTypeError(_ConfigValueError):
    """Raised when the given value config is of an invalid type"""
