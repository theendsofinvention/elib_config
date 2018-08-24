# coding=utf-8
"""
EPAB configuration exceptions
"""


class ELIBConfigError(Exception):
    """Base exception for config package"""


class IncompleteSetupError(ELIBConfigError):
    """Raised when elib_config is incomplete"""


class _ConfigFileError(ELIBConfigError):
    """Base class for all exceptions related to the config file"""

    def __init__(self, config_file_path: str, msg: str) -> None:
        self.config_file_path = config_file_path
        self.msg = msg
        super(_ConfigFileError, self).__init__(
            f'{config_file_path}: {msg}'
        )


class ConfigFileNotFoundError(_ConfigFileError):
    """Raised when the config file is missing"""

    def __init__(self, config_file_path: str) -> None:
        super(ConfigFileNotFoundError, self).__init__(
            config_file_path,
            'file not found'
        )


class InvalidConfigFileError(_ConfigFileError):
    """Raised when the format of the config file is invalid"""

    def __init__(self, config_file_path: str) -> None:
        super(InvalidConfigFileError, self).__init__(
            config_file_path,
            'config file could not be decoded; have a look at https://github.com/toml-lang/toml for the TOML '
            'language specification'
        )


class EmptyValueError(_ConfigFileError):
    """Raised when a config value in the config file is empty"""

    def __init__(self, config_file_path: str) -> None:
        super(EmptyValueError, self).__init__(
            config_file_path,
            'there is an empty value in the configuration file; look for an equal sign ("=") with no value to its right'
        )


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
