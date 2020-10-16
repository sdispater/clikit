from typing import TYPE_CHECKING

from .event import Event


if TYPE_CHECKING:
    from clikit.api.config.application_config import ApplicationConfig


class ConfigEvent(Event):
    """
    Dispatched after the configuration is built.

    Use this event to add custom configuration to the application.
    """

    def __init__(self, config):  # type: (ApplicationConfig) -> None
        self._config = config

    @property
    def config(self):  # type: () -> ApplicationConfig
        return self._config
