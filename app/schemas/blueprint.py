"""Pydantic schemas for blueprint API."""

from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel, Field, ConfigDict


class BlueprintCreate(BaseModel):
    """Schema for creating a new blueprint."""

    blueprint_string: str = Field(..., description="Encoded Factorio blueprint string")
    tags: Optional[List[str]] = Field(default=None, description="List of tag names")


class TagResponse(BaseModel):
    """Schema for tag response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class BlueprintEntityResponse(BaseModel):
    """Schema for blueprint entity response."""

    model_config = ConfigDict(from_attributes=True)

    entity_name: str
    entity_count: int


class BlueprintResponse(BaseModel):
    """Schema for blueprint response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    blueprint_string: str
    version_major: Optional[int]
    version_minor: Optional[int]
    version_patch: Optional[int]
    width: Optional[int]
    height: Optional[int]
    entity_count: Optional[int]
    created_at: datetime
    updated_at: datetime
    entities: List[BlueprintEntityResponse] = []
    tags: List[TagResponse] = []


class BlueprintListResponse(BaseModel):
    """Schema for blueprint list response (without full blueprint_string)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    width: Optional[int]
    height: Optional[int]
    entity_count: Optional[int]
    created_at: datetime
    tags: List[TagResponse] = []
