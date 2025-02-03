import logging
import os
import uvicorn
from elasticapm.handlers.logging import LoggingHandler
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

# Configure the main logger
logging.basicConfig(level=logging.DEBUG)  # Or any other level you want


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)
# Set all CORS enabled origins
# allow_origins=[
#         "http://localhost",
#         "http://localhost:3000",
#         "http://localhost:80",
#         "https://localhost",
#         "https://localhost:3000",
#         "https://localhost:80",
#
#     ]
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

apm_client = make_apm_client(
    {
        "SERVICE_NAME": "AI project Elasticsearch Monitor",
        "SERVER_URL": "http://apm-server:8200",
        "ENVIRONMENT": "development",
    }
)
@app.on_event("startup")
async def check_cors_middleware():
    cors_config = None

    # Find CORSMiddleware in middleware stack
    current_middleware = app.middleware_stack
    while current_middleware:
        if isinstance(current_middleware, CORSMiddleware):
            cors_config = current_middleware
            break  # Found it, no need to continue
        current_middleware = getattr(current_middleware, "app", None)

    if cors_config:
        print("✅ CORS Middleware Found!")
        print("🔍 Allowed Origins:", cors_config.allow_origins)
    else:
        print("❌ CORS Middleware NOT Found!")

logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.DEBUG)
if apm_client:
    # Create an Elastic APM logging handler and add it to the root logger
    apm_handler = LoggingHandler(client=apm_client)
    logger.addHandler(apm_handler)
    logging.getLogger("elasticapm").setLevel(logging.ERROR)
    # Add the Elastic APM middleware
    app.add_middleware(ElasticAPM, client=apm_client)

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
