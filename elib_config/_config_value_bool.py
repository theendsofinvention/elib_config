# coding=utf-8
"""
Config value that will be cast as a boolean
"""
# noinspection PyProtectedMember
from elib_config._config_value import ConfigValue
# noinspection PyProtectedMember
from elib_config._exc import ConfigTypeError


class ConfigValueBool(ConfigValue):
    """
    Config value that will be cast as a boolean
    """

    @property
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return 'boolean'

    def _cast(self, raw_value) -> bool:
        if not isinstance(raw_value, bool):
            raise ConfigTypeError(
                self.path,
                f'invalid boolean expression: "{raw_value}"; use either "true" or "false" instead, without the quotes.'
            )

        return raw_value
