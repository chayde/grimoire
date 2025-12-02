"""Blueprint parser for decoding Factorio blueprint strings.

Factorio blueprints are encoded as:
1. JSON object with blueprint data
2. Compressed with zlib
3. Encoded to base64
4. Prefixed with version "0"

This module decodes them and extracts useful metadata.
"""

import base64
import json
import zlib
from typing import Dict, List, Optional, Any


class BlueprintParseError(Exception):
    """Raised when blueprint string cannot be parsed."""
    pass


class BlueprintParser:
    """Parser for Factorio blueprint strings."""

    @staticmethod
    def decode(blueprint_string: str) -> Dict[str, Any]:
        """
        Decode a Factorio blueprint string.

        Args:
            blueprint_string: The encoded blueprint string (starts with "0")

        Returns:
            Decoded blueprint data as dictionary

        Raises:
            BlueprintParseError: If decoding fails
        """
        try:
            # Remove version prefix
            if not blueprint_string.startswith("0"):
                raise BlueprintParseError(
                    "Invalid blueprint string: must start with version '0'"
                )

            encoded_data = blueprint_string[1:]

            # Base64 decode
            compressed_data = base64.b64decode(encoded_data)

            # Zlib decompress
            json_data = zlib.decompress(compressed_data)

            # Parse JSON
            blueprint_data = json.loads(json_data)

            return blueprint_data

        except (base64.binascii.Error, zlib.error, json.JSONDecodeError) as e:
            raise BlueprintParseError(f"Failed to decode blueprint: {str(e)}")

    @staticmethod
    def extract_metadata(blueprint_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract useful metadata from decoded blueprint data.

        Args:
            blueprint_data: Decoded blueprint dictionary

        Returns:
            Dictionary with extracted metadata
        """
        # Handle both single blueprints and blueprint books
        if "blueprint" in blueprint_data:
            bp = blueprint_data["blueprint"]
        elif "blueprint_book" in blueprint_data:
            # For blueprint books, just extract book-level metadata
            book = blueprint_data["blueprint_book"]
            return {
                "type": "blueprint_book",
                "name": book.get("label", "Untitled Blueprint Book"),
                "description": book.get("description", ""),
                "blueprint_count": len(book.get("blueprints", [])),
            }
        else:
            raise BlueprintParseError(
                "Invalid blueprint data: missing 'blueprint' or 'blueprint_book' key"
            )

        # Extract basic info
        name = bp.get("label", "Untitled Blueprint")
        description = bp.get("description", "")
        entities = bp.get("entities", [])

        # Count entities by type
        entity_counts: Dict[str, int] = {}
        for entity in entities:
            entity_name = entity.get("name", "unknown")
            entity_counts[entity_name] = entity_counts.get(entity_name, 0) + 1

        # Calculate dimensions from entity positions
        dimensions = BlueprintParser._calculate_dimensions(entities)

        # Extract version (encoded as a 64-bit integer)
        version_int = bp.get("version", 0)
        version = BlueprintParser._decode_version(version_int)

        return {
            "type": "blueprint",
            "name": name,
            "description": description,
            "entity_count": len(entities),
            "entity_counts": entity_counts,
            "width": dimensions["width"],
            "height": dimensions["height"],
            "version_major": version["major"],
            "version_minor": version["minor"],
            "version_patch": version["patch"],
        }

    @staticmethod
    def _calculate_dimensions(entities: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate blueprint dimensions from entity positions.

        Args:
            entities: List of entity dictionaries

        Returns:
            Dictionary with width and height
        """
        if not entities:
            return {"width": 0, "height": 0}

        positions = [e.get("position", {}) for e in entities]
        xs = [p.get("x", 0) for p in positions if "x" in p]
        ys = [p.get("y", 0) for p in positions if "y" in p]

        if not xs or not ys:
            return {"width": 0, "height": 0}

        # Calculate bounding box
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Add 1 to account for the entity size (approximate)
        width = int(max_x - min_x) + 1
        height = int(max_y - min_y) + 1

        return {"width": width, "height": height}

    @staticmethod
    def _decode_version(version_int: int) -> Dict[str, int]:
        """
        Decode Factorio version from 64-bit integer.

        Format: 16 bits major, 16 bits minor, 16 bits patch, 16 bits dev

        Args:
            version_int: Version as 64-bit integer

        Returns:
            Dictionary with major, minor, patch version numbers
        """
        if version_int == 0:
            return {"major": 0, "minor": 0, "patch": 0}

        # Extract version components (simplified - actual decoding is complex)
        major = (version_int >> 48) & 0xFFFF
        minor = (version_int >> 32) & 0xFFFF
        patch = (version_int >> 16) & 0xFFFF

        return {"major": major, "minor": minor, "patch": patch}

    @classmethod
    def parse(cls, blueprint_string: str) -> Dict[str, Any]:
        """
        Convenience method to decode and extract metadata in one call.

        Args:
            blueprint_string: The encoded blueprint string

        Returns:
            Dictionary with extracted metadata

        Raises:
            BlueprintParseError: If parsing fails
        """
        blueprint_data = cls.decode(blueprint_string)
        metadata = cls.extract_metadata(blueprint_data)
        return metadata
