"""Main FastAPI application."""

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, init_db
from app.api.blueprints import router as blueprints_router
from app.services.blueprint_service import BlueprintService

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A web application for managing Factorio blueprints",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(blueprints_router)


# Initialize database on startup
@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    init_db()


# HTML page routes
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    """Home page showing recent blueprints."""
    blueprints = BlueprintService.list_blueprints(db=db, limit=10)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "blueprints": blueprints}
    )


@app.get("/upload")
async def upload_page(request: Request):
    """Blueprint upload form page."""
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )


@app.get("/blueprints/{blueprint_id}")
async def blueprint_detail(request: Request, blueprint_id: int, db: Session = Depends(get_db)):
    """Blueprint detail page."""
    blueprint = BlueprintService.get_blueprint(db=db, blueprint_id=blueprint_id)
    if not blueprint:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Blueprint not found"},
            status_code=404
        )
    return templates.TemplateResponse(
        "detail.html",
        {"request": request, "blueprint": blueprint}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}
