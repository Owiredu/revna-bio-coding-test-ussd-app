from typing import Final


# ENVIRONMENT CONFIGURATION
ENV = "dev" # "dev", "test" and "prod" for development, testing and production respectively

# SERVICE NAME AND VERSION
SERVICE_NAME: Final[str] = "USSD App"
SERVICE_VERSION: Final[str] = "1.0.0"

# CROSS-ORIGIN RESOURCE SHARING (CORS) CONFIGURATION
# FOR DEVELOPMENT
DEV_CORS_ALLOW_ORIGINS: Final[list[str]] = [
    "*"
]
DEV_CORS_ALLOW_CREDENTIALS: Final[bool] = True
DEV_CORS_ALLOW_METHODS: Final[list[str]] = [
    "GET",
    "POST",
    "OPTIONS"
]
DEV_CORS_ALLOW_HEADERS: Final[list[str]] = [
    "*"
]
# FOR TESTING
TEST_CORS_ALLOW_ORIGINS: Final[list[str]] = [
    "*"
]
TEST_CORS_ALLOW_CREDENTIALS: Final[bool] = True
TEST_CORS_ALLOW_METHODS: Final[list[str]] = [
    "GET",
    "POST",
    "OPTIONS"
]
TEST_CORS_ALLOW_HEADERS: Final[list[str]] = [
    "*"
]
# FOR PRODUCTION
PROD_CORS_ALLOW_ORIGINS: Final[list[str]] = [
    "*"
]
PROD_CORS_ALLOW_CREDENTIALS: Final[bool] = True
PROD_CORS_ALLOW_METHODS: Final[list[str]] = [
    "GET",
    "POST",
    "OPTIONS"
]
PROD_CORS_ALLOW_HEADERS: Final[list[str]] = [
    "*"
]

MNOTIFY_SMS_API_KEY: Final[str] = "0U2AsGlcB57ELNUZSOdUKsuY7"