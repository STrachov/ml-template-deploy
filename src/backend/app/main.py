import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

from elasticapm.contrib.starlette import make_apm_client, ElasticAPM






def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Configure the APM client
apm_config = {
    'SERVICE_NAME': 'JOAN Elasticsearch Monitor',
    'SERVER_URL': 'http://localhost:8200',
    'ENVIRONMENT': 'development',
    #'SECRET_TOKEN': '',
}

apm_client = make_apm_client(apm_config)

# Add the Elastic APM middleware
app.add_middleware(ElasticAPM, client=apm_client)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        reload=True,
        host='localhost',
        port=8080,
    )