"""Command-line interface for the Georgian Guide application.

This module provides a simple CLI for testing the application.
"""

import argparse
import asyncio
import os
import sys
from typing import Dict

from dotenv import load_dotenv

from georgian_guide.core.interfaces import ToolInterface
from georgian_guide.core.processor import QueryProcessor
from georgian_guide.llm.output_receiver import OpenAIOutputReceiver
from georgian_guide.llm.router import OpenAILLMRouter
from georgian_guide.schemas.base import ToolType
from georgian_guide.schemas.query import UserQuery
from georgian_guide.tools.google_maps import (
    DirectionsMapsTool,
    DistanceMatrixMapsTool,
    ElevationMapsTool,
    GeocodeMapsTool,
    PlaceDetailsMapsTool,
    ReverseGeocodeMapsTool,
    SearchPlacesMapsTool,
)


async def main():
    """Run the CLI application."""
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required.")
        sys.exit(1)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Georgian Guide AI Assistant CLI")
    parser.add_argument("query", nargs="?", help="The query to process")
    args = parser.parse_args()
    
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
    processor = QueryProcessor(
        router=router,
        output_receiver=output_receiver,
        tools=tools
    )
    
    # Process query from arguments or prompt for input
    if args.query:
        query_text = args.query
    else:
        query_text = input("Enter your query: ")
    
    # Create user query
    user_query = UserQuery(query=query_text)
    
    print("\nProcessing query...\n")
    
    try:
        # Process the query
        response = await processor.process_query(user_query)
        
        # Print the response
        print("=" * 80)
        print("RESPONSE:")
        print("=" * 80)
        print(response.response)
        print("\n")
        
        if response.follow_up_questions:
            print("Follow-up Questions:")
            for i, question in enumerate(response.follow_up_questions, 1):
                print(f"{i}. {question}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 