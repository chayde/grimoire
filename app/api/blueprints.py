"""Blueprint API endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.blueprint import (
    BlueprintCreate,
    BlueprintResponse,
    BlueprintListResponse,
)
from app.services.blueprint_service import BlueprintService
from app.services.blueprint_parser import BlueprintParseError

router = APIRouter(prefix="/api/blueprints", tags=["blueprints"])


@router.post("/", response_model=BlueprintResponse, status_code=201)
def create_blueprint(
    blueprint_data: BlueprintCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new blueprint.

    Upload a Factorio blueprint string and optionally add tags.
    The blueprint will be parsed and metadata will be extracted automatically.
    """
    try:
        blueprint = BlueprintService.create_blueprint(
            db=db,
            blueprint_string=blueprint_data.blueprint_string,
            tag_names=blueprint_data.tags,
        )
        return blueprint
    except BlueprintParseError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[BlueprintListResponse])
def list_blueprints(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records"),
    entity: Optional[str] = Query(None, description="Filter by entity name"),
    tag: Optional[str] = Query(None, description="Filter by tag name"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    db: Session = Depends(get_db)
):
    """
    List blueprints with optional filtering.

    - **skip**: Pagination offset
    - **limit**: Maximum results (1-100)
    - **entity**: Filter by entity name (e.g., "assembling-machine-2")
    - **tag**: Filter by tag name
    - **search**: Search text in name and description
    """
    blueprints = BlueprintService.list_blueprints(
        db=db,
        skip=skip,
        limit=limit,
        entity_filter=entity,
        tag_filter=tag,
        search=search,
    )
    return blueprints


@router.get("/{blueprint_id}", response_model=BlueprintResponse)
def get_blueprint(
    blueprint_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific blueprint by ID.

    Returns full blueprint details including the encoded blueprint string.
    """
    blueprint = BlueprintService.get_blueprint(db=db, blueprint_id=blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return blueprint


@router.delete("/{blueprint_id}", status_code=204)
def delete_blueprint(
    blueprint_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a blueprint.

    Returns 204 No Content on success, 404 if blueprint not found.
    """
    deleted = BlueprintService.delete_blueprint(db=db, blueprint_id=blueprint_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return None
