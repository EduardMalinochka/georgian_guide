"""Base schemas for the Georgian Guide application.

This module defines the core schema models that are used throughout the application.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ToolType(str, Enum):
    """Enumeration of available Google Maps MCP tool types."""
    
    GEOCODE = "geocode"
    REVERSE_GEOCODE = "reverse_geocode"
    SEARCH_PLACES = "search_places"
    PLACE_DETAILS = "place_details"
    DISTANCE_MATRIX = "distance_matrix"
    ELEVATION = "elevation"
    DIRECTIONS = "directions"


class Location(BaseModel):
    """Schema representing a geographic location."""
    
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")


class Address(BaseModel):
    """Schema representing a formatted address."""
    
    formatted_address: str = Field(..., description="Fully formatted address")
    country: Optional[str] = Field(None, description="Country name")
    administrative_area: Optional[str] = Field(None, description="Administrative area")
    locality: Optional[str] = Field(None, description="City or locality")
    postal_code: Optional[str] = Field(None, description="Postal code")
    route: Optional[str] = Field(None, description="Street or route")
    street_number: Optional[str] = Field(None, description="Street number")


class Place(BaseModel):
    """Schema representing a place result from Google Maps."""
    
    place_id: str = Field(..., description="Unique identifier for the place")
    name: str = Field(..., description="Name of the place")
    location: Location = Field(..., description="Geographic coordinates")
    address: Optional[str] = Field(None, description="Formatted address")
    types: List[str] = Field(default_factory=list, description="Place types")
    rating: Optional[float] = Field(None, description="Average rating (1.0 to 5.0)")
    user_ratings_total: Optional[int] = Field(None, description="Total number of ratings")
    price_level: Optional[int] = Field(None, description="Price level (0 to 4)")
    vicinity: Optional[str] = Field(None, description="Simplified address")
    photos: Optional[List[Dict[str, Any]]] = Field(None, description="Photo references")
    opening_hours: Optional[Dict[str, Any]] = Field(None, description="Opening hours information")


class TravelMode(str, Enum):
    """Enumeration of available travel modes."""
    
    DRIVING = "driving"
    WALKING = "walking"
    BICYCLING = "bicycling"
    TRANSIT = "transit"


class DistanceMatrixElement(BaseModel):
    """Schema representing a distance matrix result element."""
    
    distance: Dict[str, Union[str, int]] = Field(..., description="Distance information")
    duration: Dict[str, Union[str, int]] = Field(..., description="Duration information")
    status: str = Field(..., description="Status of this result")


class DirectionsResult(BaseModel):
    """Schema representing directions result."""
    
    summary: str = Field(..., description="Summary of the route")
    distance: Dict[str, Union[str, int]] = Field(..., description="Distance information")
    duration: Dict[str, Union[str, int]] = Field(..., description="Duration information")
    steps: List[Dict[str, Any]] = Field(..., description="Steps in the route")


class ElevationResult(BaseModel):
    """Schema representing elevation result."""
    
    elevation: float = Field(..., description="Elevation in meters")
    location: Location = Field(..., description="Location for this elevation")
    resolution: float = Field(..., description="Maximum distance between data points") 