from enum import Enum


class EnvironmentEnum(str, Enum):
    """Enumeration for different environments."""

    production = "production"
    development = "development"


class DefaultFoldersEnum(str, Enum):
    """Enumeration for default folders."""

    data = "data"
    generated = "generated"
