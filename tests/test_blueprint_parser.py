"""Tests for blueprint parser."""

import base64
import json
import zlib

import pytest
from app.services.blueprint_parser import BlueprintParser, BlueprintParseError


def create_test_blueprint() -> str:
    """Create a valid test blueprint string."""
    blueprint_data = {
        "blueprint": {
            "item": "blueprint",
            "label": "Test Blueprint",
            "description": "A test blueprint for unit testing",
            "entities": [
                {
                    "entity_number": 1,
                    "name": "transport-belt",
                    "position": {"x": 0.5, "y": 0.5}
                },
                {
                    "entity_number": 2,
                    "name": "inserter",
                    "position": {"x": 2.5, "y": 0.5}
                }
            ],
            "version": 281474976710656  # Version 1.0.0
        }
    }

    # Encode it: JSON -> zlib -> base64 -> add "0" prefix
    json_str = json.dumps(blueprint_data)
    compressed = zlib.compress(json_str.encode('utf-8'))
    encoded = base64.b64encode(compressed).decode('utf-8')
    return "0" + encoded


SAMPLE_BLUEPRINT = create_test_blueprint()


def test_decode_valid_blueprint():
    """Test decoding a valid blueprint string."""
    result = BlueprintParser.decode(SAMPLE_BLUEPRINT)

    assert isinstance(result, dict)
    assert "blueprint" in result
    assert result["blueprint"]["label"] == "Test Blueprint"


def test_decode_invalid_prefix():
    """Test that blueprint without '0' prefix raises error."""
    with pytest.raises(BlueprintParseError, match="must start with version"):
        BlueprintParser.decode("invalid_blueprint")


def test_decode_invalid_base64():
    """Test that invalid base64 raises error."""
    with pytest.raises(BlueprintParseError, match="Failed to decode"):
        BlueprintParser.decode("0!@#$%^&*()")


def test_extract_metadata():
    """Test extracting metadata from decoded blueprint."""
    blueprint_data = BlueprintParser.decode(SAMPLE_BLUEPRINT)
    metadata = BlueprintParser.extract_metadata(blueprint_data)

    assert metadata["type"] == "blueprint"
    assert isinstance(metadata["name"], str)
    assert isinstance(metadata["entity_count"], int)
    assert isinstance(metadata["entity_counts"], dict)
    assert "width" in metadata
    assert "height" in metadata


def test_parse_convenience_method():
    """Test the convenience parse() method."""
    metadata = BlueprintParser.parse(SAMPLE_BLUEPRINT)

    assert "name" in metadata
    assert "entity_count" in metadata
    assert metadata["type"] == "blueprint"


def test_calculate_dimensions_empty():
    """Test dimension calculation with no entities."""
    dimensions = BlueprintParser._calculate_dimensions([])

    assert dimensions["width"] == 0
    assert dimensions["height"] == 0


def test_calculate_dimensions_single_entity():
    """Test dimension calculation with one entity."""
    entities = [{"position": {"x": 5.5, "y": 3.5}}]
    dimensions = BlueprintParser._calculate_dimensions(entities)

    assert dimensions["width"] == 1
    assert dimensions["height"] == 1


def test_calculate_dimensions_multiple_entities():
    """Test dimension calculation with multiple entities."""
    entities = [
        {"position": {"x": 0, "y": 0}},
        {"position": {"x": 5, "y": 3}},
    ]
    dimensions = BlueprintParser._calculate_dimensions(entities)

    assert dimensions["width"] == 6
    assert dimensions["height"] == 4


def test_decode_version():
    """Test version decoding."""
    # Version 1.1.0 encoded
    version = BlueprintParser._decode_version(281474976710656)

    assert isinstance(version, dict)
    assert "major" in version
    assert "minor" in version
    assert "patch" in version
