from enum import Enum, auto
from pathlib import Path

from envkit import Env

ROOT_DIRECTORY = Path(__file__).parent.parent


class Environment(Enum):
    DEVELOPMENT = auto()
    PRODUCTION = auto()

    def is_development(self) -> bool:
        return self == Environment.DEVELOPMENT

    def is_production(self) -> bool:
        return self == Environment.PRODUCTION


environment = Env.enum(
    "ENVIRONMENT", Environment, required=False, default=Environment.DEVELOPMENT
)
port = Env.int("PORT", required=False, default=8080)
