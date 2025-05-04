"""Tool schemas for the Georgian Guide application.

This module defines the schema models for Google Maps MCP tools.
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from georgian_guide.schemas.base import Location, TravelMode


class GeocodeRequest(BaseModel):
    """Schema for Google Maps geocode request."""
    
    address: str = Field(..., description="The address to geocode")


class GeocodeResponse(BaseModel):
    """Schema for Google Maps geocode response."""
    
    results: List[Dict[str, Any]] = Field(..., description="Geocoding results")
    status: str = Field(..., description="Status of the geocoding request")


class ReverseGeocodeRequest(BaseModel):
    """Schema for Google Maps reverse geocode request."""
    
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")


class ReverseGeocodeResponse(BaseModel):
    """Schema for Google Maps reverse geocode response."""
    
    results: List[Dict[str, Any]] = Field(..., description="Reverse geocoding results")
    status: str = Field(..., description="Status of the reverse geocoding request")


class PlacesSearchRequest(BaseModel):
    """Schema for Google Maps places search request."""
    
    query: str = Field(..., description="Search query")
    location: Optional[Location] = Field(None, description="Optional center point for the search")
    radius: Optional[float] = Field(None, description="Search radius in meters (max 50000)")


class PlacesSearchResponse(BaseModel):
    """Schema for Google Maps places search response."""
    
    results: List[Dict[str, Any]] = Field(..., description="Places search results")
    status: str = Field(..., description="Status of the places search request")


class PlaceDetailsRequest(BaseModel):
    """Schema for Google Maps place details request."""
    
    place_id: str = Field(..., description="The place ID to get details for")


class PlaceDetailsResponse(BaseModel):
    """Schema for Google Maps place details response."""
    
    result: Dict[str, Any] = Field(..., description="Place details result")
    status: str = Field(..., description="Status of the place details request")


class DistanceMatrixRequest(BaseModel):
    """Schema for Google Maps distance matrix request."""
    
    origins: List[str] = Field(..., description="Array of origin addresses or coordinates")
    destinations: List[str] = Field(..., description="Array of destination addresses or coordinates")
    mode: Optional[TravelMode] = Field(None, description="Travel mode")


class DistanceMatrixResponse(BaseModel):
    """Schema for Google Maps distance matrix response."""
    
    origin_addresses: List[str] = Field(..., description="List of origin addresses")
    destination_addresses: List[str] = Field(..., description="List of destination addresses")
    rows: List[Dict[str, Any]] = Field(..., description="Matrix of results")
    status: str = Field(..., description="Status of the distance matrix request")


class ElevationRequest(BaseModel):
    """Schema for Google Maps elevation request."""
    
    locations: List[Location] = Field(..., description="Array of locations to get elevation for")


class ElevationResponse(BaseModel):
    """Schema for Google Maps elevation response."""
    
    results: List[Dict[str, Any]] = Field(..., description="Elevation results")
    status: str = Field(..., description="Status of the elevation request")


class DirectionsRequest(BaseModel):
    """Schema for Google Maps directions request."""
    
    origin: str = Field(..., description="Starting point address or coordinates")
    destination: str = Field(..., description="Ending point address or coordinates")
    mode: Optional[TravelMode] = Field(None, description="Travel mode")


class DirectionsResponse(BaseModel):
    """Schema for Google Maps directions response."""
    
    routes: List[Dict[str, Any]] = Field(..., description="Directions routes")
    status: str = Field(..., description="Status of the directions request") 