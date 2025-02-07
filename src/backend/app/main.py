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
import boto3

# Set AWS Region
AWS_REGION = "eu-north-1"
LOG_GROUP_NAME = "fastapi-log-group"
LOG_STREAM_NAME = "fastapi-log-stream"

# Initialize CloudWatch client
cloudwatch_logs = boto3.client("logs", region_name=AWS_REGION)

def setup_cloudwatch_logging():
    try:
        cloudwatch_logs.create_log_group(logGroupName=LOG_GROUP_NAME)
    except cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
        pass  # Log group exists

    try:
        cloudwatch_logs.create_log_stream(logGroupName=LOG_GROUP_NAME, logStreamName=LOG_STREAM_NAME)
    except cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
        pass  # Log stream exists

setup_cloudwatch_logging()

class CloudWatchLogHandler(logging.Handler):
    """Custom log handler for AWS CloudWatch Logs."""

    def emit(self, record):
        log_entry = self.format(record)
        try:
            cloudwatch_logs.put_log_events(
                logGroupName=LOG_GROUP_NAME,
                logStreamName=LOG_STREAM_NAME,
                logEvents=[{"timestamp": int(record.created * 1000), "message": log_entry}],
            )
        except Exception as e:
            print(f"Failed to send logs to CloudWatch: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastapi-app")
logger.setLevel(logging.INFO)

# Attach CloudWatch log handler
cloudwatch_handler = CloudWatchLogHandler()
cloudwatch_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(cloudwatch_handler)

# Test log message
logger.info("✅ Testing CloudWatch Logs from Local Machine!")

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


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
#
# apm_client = make_apm_client(
#     {
#         "SERVICE_NAME": "AI project Elasticsearch Monitor",
#         "SERVER_URL": "http://apm-server:8200",
#         "ENVIRONMENT": "development",
#     }
# )
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

# if apm_client:
#     # Create an Elastic APM logging handler and add it to the root logger
#     apm_handler = LoggingHandler(client=apm_client)
#     logger.addHandler(apm_handler)
#     logging.getLogger("elasticapm").setLevel(logging.ERROR)
#     # Add the Elastic APM middleware
#     app.add_middleware(ElasticAPM, client=apm_client)

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
