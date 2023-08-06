from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from kisters.network_store.service.dm.settings import settings

from .routing import networks, schemas

API_PATH = "/rest"


app = FastAPI(
    title="Network Store REST API",
    description="Storage service for directed graph infrastructure networks",
    docs_url=None,
    redoc_url=f"{API_PATH}/redoc",
    openapi_url=f"{API_PATH}/openapi.json",
    default_response_class=ORJSONResponse,
)


# Mount Static Files
static = Path(__file__).parent.resolve() / "static"
app.mount("/static", StaticFiles(directory=static), name="static")

dependencies = []

if settings.enable_access_control:
    from kisters.water.operational.access_control.fastapi import TokenAuthenticator

    authenticator = TokenAuthenticator(
        allowed_origin=f"{settings.deployment_url}{API_PATH}/*"
    )
    dependencies.append(Depends(authenticator))

app.include_router(
    networks,
    prefix=f"{API_PATH}/networks",
    tags=["networks"],
    dependencies=dependencies,
)
app.include_router(
    schemas,
    prefix=f"{API_PATH}/schemas",
    tags=["schemas"],
    dependencies=dependencies,
)

if settings.enable_viewer:
    from .viewer import viewer

    app.include_router(
        viewer,
        prefix=f"{API_PATH}",
        tags=["viewer"],
        dependencies=dependencies,
    )

    @app.get(f"{API_PATH}/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )


@app.get("/", include_in_schema=False)
async def docs_redirect_root():
    return RedirectResponse(url=f"{API_PATH}/docs")


@app.get(API_PATH, include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url=f"{API_PATH}/docs")
