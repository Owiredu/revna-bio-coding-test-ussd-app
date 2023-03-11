from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import config
from routers import user, ussd


# create the fastAPI instance
app = FastAPI(title=config.SERVICE_NAME, version=config.SERVICE_VERSION)


# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOW_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS
)


# add routers
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(ussd.router, prefix="/ussd", tags=["ussd"])
