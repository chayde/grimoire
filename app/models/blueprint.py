"""Blueprint database models."""

from datetime import datetime
from typing import List

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Table,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


# Association table for many-to-many relationship between blueprints and tags
blueprint_tags = Table(
    "blueprint_tags",
    Base.metadata,
    Column("blueprint_id", Integer, ForeignKey("blueprints.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Index("idx_blueprint_tags_blueprint_id", "blueprint_id"),
    Index("idx_blueprint_tags_tag_id", "tag_id"),
)


class Blueprint(Base):
    """Blueprint model for storing Factorio blueprints."""

    __tablename__ = "blueprints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    blueprint_string: Mapped[str] = mapped_column(Text, nullable=False)

    # Calculated from parsed blueprint
    version_major: Mapped[int] = mapped_column(Integer, nullable=True)
    version_minor: Mapped[int] = mapped_column(Integer, nullable=True)
    version_patch: Mapped[int] = mapped_column(Integer, nullable=True)
    width: Mapped[int] = mapped_column(Integer, nullable=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    entity_count: Mapped[int] = mapped_column(Integer, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    entities: Mapped[List["BlueprintEntity"]] = relationship(
        "BlueprintEntity", back_populates="blueprint", cascade="all, delete-orphan"
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=blueprint_tags, back_populates="blueprints"
    )

    def __repr__(self) -> str:
        return f"<Blueprint(id={self.id}, name='{self.name}')>"


class BlueprintEntity(Base):
    """Entity counts for each blueprint."""

    __tablename__ = "blueprint_entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    blueprint_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("blueprints.id", ondelete="CASCADE"), nullable=False, index=True
    )
    entity_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    blueprint: Mapped["Blueprint"] = relationship("Blueprint", back_populates="entities")

    # Unique constraint: one entry per entity type per blueprint
    __table_args__ = (
        UniqueConstraint("blueprint_id", "entity_name", name="uq_blueprint_entity"),
    )

    def __repr__(self) -> str:
        return f"<BlueprintEntity(blueprint_id={self.blueprint_id}, entity='{self.entity_name}', count={self.entity_count})>"


class Tag(Base):
    """Tags for categorizing blueprints."""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    # Relationships
    blueprints: Mapped[List["Blueprint"]] = relationship(
        "Blueprint", secondary=blueprint_tags, back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name='{self.name}')>"
