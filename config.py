from typing import Final


# SERVICE NAME AND VERSION
SERVICE_NAME: Final[str] = "USSD App"
SERVICE_VERSION: Final[str] = "1.0.0"

# CROSS-ORIGIN RESOURCE SHARING (CORS) CONFIGURATION
CORS_ALLOW_ORIGINS: Final[list[str]] = [
    "*"
]
CORS_ALLOW_CREDENTIALS: Final[bool] = True
CORS_ALLOW_METHODS: Final[list[str]] = [
    "GET",
    "POST",
    "OPTIONS"
]
CORS_ALLOW_HEADERS: Final[list[str]] = [
    "*"
]

MNOTIFY_SMS_API_KEY: Final[str] = "0U2AsGlcB57ELNUZSOdUKsuY7"