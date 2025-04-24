from enum import Enum


class EnvironmentEnum(str, Enum):
    production = "production"
    development = "development"


class DefaultFoldersEnum(str, Enum):
    data = "data"
    generated = "generated"
