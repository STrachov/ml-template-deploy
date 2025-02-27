import logging
import os
from logging.handlers import RotatingFileHandler

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")

# Setup Logger
logger = logging.getLogger("fastapi-app")

if not logger.hasHandlers():


    # Console Handler (logs to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Rotating File Handler (logs to file, max 10MB, overwrites)
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=0, delay=False)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
# Test Logs
logger.info("Logging initialized. App log stored at: " + log_file)
logger.warning("This is a warning message")
logger.error("This is an error message")

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

# Sync FastAPI logs with your logger
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = logging.getLogger("fastapi-app").handlers
uvicorn_logger.setLevel(logging.INFO)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_STR)

# uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
#
# if __name__ == "__main__":
#     uvicorn.run(
#         "app.main:app",
#         reload=True,
#         host=settings.BACKEND_HOST,
#         port=settings.BACKEND_PORT,
#     )
