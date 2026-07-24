
"""
Q Signals - Dependency Injection

Centralized FastAPI dependencies.

Only dependencies for existing modules should be added here.
As new services are created, expose them through this module.
"""

from typing import Annotated

from fastapi import Depends

from app.core.config import config
from app.core.settings import Settings, settings


def get_settings() -> Settings:
    """
    Return the singleton application settings.
    """
    return settings


def get_config():
    """
    Return the centralized application configuration.
    """
    return config


# ---------------------------------------------------------------------
# Dependency Aliases
# ---------------------------------------------------------------------

SettingsDependency = Annotated[Settings, Depends(get_settings)]

ConfigDependency = Annotated[type(config), Depends(get_config)]

