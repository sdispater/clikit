from typing import Optional

from .api.config.application_config import ApplicationConfig
from .console_application import ConsoleApplication
from .config.default_application_config import DefaultApplicationConfig


__version__ = "0.1.0"


def application(
    config=None
):  # type: (Optional[ApplicationConfig]) -> ConsoleApplication
    if config is None:
        config = DefaultApplicationConfig()

    return ConsoleApplication(config)
