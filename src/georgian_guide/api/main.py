"""Main API module for the Georgian Guide application.

This module defines the FastAPI application and endpoints.
"""

import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from georgian_guide.core.interfaces import ToolInterface
from georgian_guide.core.processor import QueryProcessor
from georgian_guide.llm.output_receiver import OpenAIOutputReceiver
from georgian_guide.llm.router import OpenAILLMRouter
from georgian_guide.schemas.base import ToolType
from georgian_guide.schemas.query import AssistantResponse, UserQuery
from georgian_guide.tools.google_maps import (
    DirectionsMapsTool,
    DistanceMatrixMapsTool,
    ElevationMapsTool,
    GeocodeMapsTool,
    PlaceDetailsMapsTool,
    ReverseGeocodeMapsTool,
    SearchPlacesMapsTool,
)

# Load environment variables from .env file
load_dotenv()

# Check for required API keys
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Get the directory of the static files
current_dir = Path(__file__).parent
static_dir = current_dir / "static"

# Create FastAPI application
app = FastAPI(
    title="Georgian Guide AI Assistant API",
    description="API for the Georgian Guide AI Assistant",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Initialize components on startup
@app.on_event("startup")
async def startup_event():
    """Initialize application components on startup."""
    # Create tool instances
    tools: Dict[ToolType, ToolInterface] = {
        ToolType.GEOCODE: GeocodeMapsTool(),
        ToolType.REVERSE_GEOCODE: ReverseGeocodeMapsTool(),
        ToolType.SEARCH_PLACES: SearchPlacesMapsTool(),
        ToolType.PLACE_DETAILS: PlaceDetailsMapsTool(),
        ToolType.DISTANCE_MATRIX: DistanceMatrixMapsTool(),
        ToolType.ELEVATION: ElevationMapsTool(),
        ToolType.DIRECTIONS: DirectionsMapsTool(),
    }
    
    # Create router and output receiver
    router = OpenAILLMRouter()
    output_receiver = OpenAIOutputReceiver()
    
    # Create query processor
    app.state.processor = QueryProcessor(
        router=router,
        output_receiver=output_receiver,
        tools=tools
    )


@app.post("/query", response_model=AssistantResponse)
async def process_query(query: UserQuery) -> AssistantResponse:
    """Process a user query using POST.
    
    Args:
        query: The user query
        
    Returns:
        Assistant response
    """
    try:
        return await app.state.processor.process_query(query)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/api/ask", response_model=AssistantResponse)
async def get_query(query: str) -> AssistantResponse:
    """Process a user query using GET.
    
    Args:
        query: The user query as a query parameter
        
    Returns:
        Assistant response
    """
    try:
        user_query = UserQuery(query=query)
        return await app.state.processor.process_query(user_query)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the index.html file.
    
    Returns:
        HTML content
    """
    html_file = static_dir / "index.html"
    if html_file.exists():
        with open(html_file, "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    else:
        raise HTTPException(
            status_code=404, 
            detail="Index file not found"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("georgian_guide.api.main:app", host="0.0.0.0", port=8000, reload=True) 