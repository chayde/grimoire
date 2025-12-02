"""Blueprint service for business logic."""

from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.blueprint import Blueprint, BlueprintEntity, Tag
from app.services.blueprint_parser import BlueprintParser, BlueprintParseError


class BlueprintService:
    """Service for managing blueprints."""

    @staticmethod
    def create_blueprint(
        db: Session,
        blueprint_string: str,
        tag_names: Optional[List[str]] = None
    ) -> Blueprint:
        """
        Create a new blueprint from encoded string.

        Args:
            db: Database session
            blueprint_string: Encoded blueprint string
            tag_names: Optional list of tag names

        Returns:
            Created Blueprint object

        Raises:
            BlueprintParseError: If blueprint string is invalid
        """
        # Parse the blueprint
        metadata = BlueprintParser.parse(blueprint_string)

        # Create blueprint record
        blueprint = Blueprint(
            name=metadata["name"],
            description=metadata["description"],
            blueprint_string=blueprint_string,
            version_major=metadata["version_major"],
            version_minor=metadata["version_minor"],
            version_patch=metadata["version_patch"],
            width=metadata["width"],
            height=metadata["height"],
            entity_count=metadata["entity_count"],
        )

        db.add(blueprint)
        db.flush()  # Get blueprint.id without committing

        # Add entity counts
        for entity_name, count in metadata["entity_counts"].items():
            entity = BlueprintEntity(
                blueprint_id=blueprint.id,
                entity_name=entity_name,
                entity_count=count,
            )
            db.add(entity)

        # Add tags
        if tag_names:
            for tag_name in tag_names:
                # Get or create tag
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                blueprint.tags.append(tag)

        db.commit()
        db.refresh(blueprint)

        return blueprint

    @staticmethod
    def get_blueprint(db: Session, blueprint_id: int) -> Optional[Blueprint]:
        """
        Get a blueprint by ID.

        Args:
            db: Database session
            blueprint_id: Blueprint ID

        Returns:
            Blueprint or None if not found
        """
        return db.query(Blueprint).filter(Blueprint.id == blueprint_id).first()

    @staticmethod
    def list_blueprints(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        entity_filter: Optional[str] = None,
        tag_filter: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Blueprint]:
        """
        List blueprints with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            entity_filter: Filter by entity name
            tag_filter: Filter by tag name
            search: Search in name and description

        Returns:
            List of blueprints
        """
        query = db.query(Blueprint)

        # Filter by entity
        if entity_filter:
            query = query.join(Blueprint.entities).filter(
                BlueprintEntity.entity_name == entity_filter
            )

        # Filter by tag
        if tag_filter:
            query = query.join(Blueprint.tags).filter(Tag.name == tag_filter)

        # Search in name and description
        if search:
            query = query.filter(
                or_(
                    Blueprint.name.ilike(f"%{search}%"),
                    Blueprint.description.ilike(f"%{search}%")
                )
            )

        # Order by most recent first
        query = query.order_by(Blueprint.created_at.desc())

        # Pagination
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def delete_blueprint(db: Session, blueprint_id: int) -> bool:
        """
        Delete a blueprint.

        Args:
            db: Database session
            blueprint_id: Blueprint ID

        Returns:
            True if deleted, False if not found
        """
        blueprint = db.query(Blueprint).filter(Blueprint.id == blueprint_id).first()
        if blueprint:
            db.delete(blueprint)
            db.commit()
            return True
        return False

    @staticmethod
    def get_all_tags(db: Session) -> List[Tag]:
        """
        Get all tags.

        Args:
            db: Database session

        Returns:
            List of all tags
        """
        return db.query(Tag).order_by(Tag.name).all()
