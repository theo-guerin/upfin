from enum import Enum, auto
from pathlib import Path

from envkit import Env

ROOT_DIRECTORY = Path(__file__).parent.parent

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {
            "()": "asgi_correlation_id.CorrelationIdFilter",
            "uuid_length": 32,
            "default_value": "-",
        },
    },
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(correlation_id)s] %(levelname)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["correlation_id"],
            "formatter": "standard",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}


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

jellyfin_api_base_url = Env.str("JELLYFIN_API_BASE_URL")
jellyfin_api_key = Env.str("JELLYFIN_API_KEY")
jellyfin_movie_library_path = Path(Env.str("JELLYFIN_MOVIE_LIBRARY_PATH"))
