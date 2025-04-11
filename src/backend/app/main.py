import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from contextlib import asynccontextmanager

#import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from app.api.main import api_router
from app.core.config import settings

# Create a structured logger setup
def setup_logging():
    # Create logs directory 
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "app.log"
    
    # Create root logger
    logger = logging.getLogger("fastapi-app")
    
    # Only add handlers if none exist
    if not logger.handlers:
        # Configure log formatting - structured format
        log_format = "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
        formatter = logging.Formatter(log_format)
        
        # Console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,  # Keep 5 backup logs
            delay=False
        )
        file_handler.setFormatter(formatter)
        
        # Set log levels based on environment
        if settings.ENVIRONMENT == "production":
            logger.setLevel(logging.WARNING)
            console_handler.setLevel(logging.WARNING)
            file_handler.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.INFO)
            console_handler.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
        
        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        # Make uvicorn use our logger
        uvicorn_logger = logging.getLogger("uvicorn")
        uvicorn_logger.handlers = logger.handlers
        
        # Make sqlalchemy less verbose
        logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
        
        logger.info(f"Logging initialized. Environment: {settings.ENVIRONMENT}")
    
    return logger

# Setup logger
logger = setup_logging()

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME}")
    logger.info(f"API running at {settings.API_V1_STR}")
    logger.info(f"CORS origins: {settings.all_cors_origins}")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    swagger_ui_init_oauth={
         "appName": settings.PROJECT_NAME,
    },
    lifespan=lifespan,
)

# Add CORS middleware
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include the API router
app.include_router(api_router, prefix=settings.API_V1_STR)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="API documentation",
        routes=app.routes,
    )
    
    # Initialize components if it doesn't exist
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
        
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": f"{settings.API_V1_STR}/login/access-token",
                    "scopes": {}
                }
            }
        }
    }
    
    # Add security requirement
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

#uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload

# if __name__ == "__main__":
#     uvicorn.run(
#         "app.main:app",
#         reload=True,
#         host=settings.BACKEND_HOST,
#         port=settings.BACKEND_PORT,
#     )
