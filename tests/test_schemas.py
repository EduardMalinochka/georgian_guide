"""Tests for the schemas module."""

from georgian_guide.schemas.base import Location, Place, ToolType
from georgian_guide.schemas.query import UserQuery, ToolCall, ToolParameter


def test_location_schema():
    """Test the Location schema."""
    location = Location(latitude=41.7151, longitude=44.8271)
    assert location.latitude == 41.7151
    assert location.longitude == 44.8271
    
    # Test dictionary conversion
    location_dict = location.dict()
    assert location_dict["latitude"] == 41.7151
    assert location_dict["longitude"] == 44.8271


def test_user_query_schema():
    """Test the UserQuery schema."""
    query = UserQuery(query="I want to eat khinkali in Tbilisi")
    assert query.query == "I want to eat khinkali in Tbilisi"
    assert query.language == "en"  # Default value
    assert query.user_id is None
    assert query.location is None


def test_tool_call_schema():
    """Test the ToolCall schema."""
    parameters = [
        ToolParameter(name="query", value="khinkali Tbilisi"),
        ToolParameter(name="radius", value=5000)
    ]
    
    tool_call = ToolCall(
        tool_type=ToolType.SEARCH_PLACES,
        parameters=parameters,
        explanation="Searching for khinkali restaurants in Tbilisi"
    )
    
    assert tool_call.tool_type == ToolType.SEARCH_PLACES
    assert len(tool_call.parameters) == 2
    assert tool_call.parameters[0].name == "query"
    assert tool_call.parameters[0].value == "khinkali Tbilisi"
    assert tool_call.explanation == "Searching for khinkali restaurants in Tbilisi"


def test_place_schema():
    """Test the Place schema."""
    place = Place(
        place_id="ChIJa-NJ6tqdnUARhLZA13JXZ4A",
        name="Sakhinkle",
        location=Location(latitude=41.6956, longitude=44.8048),
        rating=4.7,
        types=["restaurant", "food"]
    )
    
    assert place.place_id == "ChIJa-NJ6tqdnUARhLZA13JXZ4A"
    assert place.name == "Sakhinkle"
    assert place.location.latitude == 41.6956
    assert place.location.longitude == 44.8048
    assert place.rating == 4.7
    assert "restaurant" in place.types 