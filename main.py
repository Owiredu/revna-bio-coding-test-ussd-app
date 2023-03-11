from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import config
from routers import user, ussd


# create the fastAPI instance
app = FastAPI(title=config.SERVICE_NAME, version=config.SERVICE_VERSION)


# add middleware
if config.ENV == "dev":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.DEV_CORS_ALLOW_ORIGINS,
        allow_credentials=config.DEV_CORS_ALLOW_CREDENTIALS,
        allow_methods=config.DEV_CORS_ALLOW_METHODS,
        allow_headers=config.DEV_CORS_ALLOW_HEADERS
    )
elif config.ENV == "test":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.TEST_CORS_ALLOW_ORIGINS,
        allow_credentials=config.TEST_CORS_ALLOW_CREDENTIALS,
        allow_methods=config.TEST_CORS_ALLOW_METHODS,
        allow_headers=config.TEST_CORS_ALLOW_HEADERS
    )
elif config.ENV == "prod":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.PROD_CORS_ALLOW_ORIGINS,
        allow_credentials=config.PROD_CORS_ALLOW_CREDENTIALS,
        allow_methods=config.PROD_CORS_ALLOW_METHODS,
        allow_headers=config.PROD_CORS_ALLOW_HEADERS
    )


# add routers
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(ussd.router, prefix="/ussd", tags=["ussd"])
