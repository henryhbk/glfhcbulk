import os
from os.path import dirname, abspath
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    The `Settings` class represents the configuration settings for the application. It is a subclass of the `BaseSettings` class.

    Attributes:
        - DATABASE (str): Specifies the database file name.

    Nested Class:
        - Config: Specifies additional configuration options for the application.

        Config Attributes:
            - case_sensitive (bool): Determines whether the application is case-sensitive in reading configuration variables.
            - env_file (str): Specifies the file path for the environment variables.

    Usage:
        settings = Settings()

    """
    DATABASE = 'bulk_update_admin.sqlite'

    class Config:
        case_sensitive = False
        env_file = os.path.join(dirname(dirname(abspath(__file__))), '.env')


@lru_cache()
def get_settings() -> Settings:
    """
    Get settings.

    :return: Instance of Settings.
    :rtype: Settings
    """
    return Settings()
