"""LLM router implementation for the Georgian Guide application.

This module implements the LLM-based router that analyzes user queries and selects
appropriate tools.
"""

import json
import os
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from georgian_guide.core.interfaces import RouterInterface
from georgian_guide.schemas.base import Location, ToolType
from georgian_guide.schemas.query import RouterResponse, ToolCall, ToolParameter, UserQuery


class OpenAILLMRouter(RouterInterface):
    """Router implementation using OpenAI's API."""
    
    def __init__(self, model: str = "gpt-4o"):
        """Initialize the router.
        
        Args:
            model: The OpenAI model to use for routing
        """
        self.model = model
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Define the system message that instructs the LLM on how to route queries
        self.system_message = """
You are an AI assistant for travelers in Georgia (the country). Your job is to help
users find places to visit, restaurants, attractions, and other points of interest.

You have access to the following Google Maps tools:

1. GEOCODE: Convert an address into geographic coordinates
2. REVERSE_GEOCODE: Convert coordinates into an address
3. SEARCH_PLACES: Search for places using keyword queries
4. PLACE_DETAILS: Get detailed information about a specific place
5. DISTANCE_MATRIX: Calculate travel distance and time between origins and destinations
6. ELEVATION: Get elevation data for locations
7. DIRECTIONS: Get directions between two points

Analyze the user's query and select the most appropriate tool(s) to use.
For each tool, provide the necessary parameters.

YOUR RESPONSE MUST BE VALID JSON in the following format:
{
  "selected_tools": [
    {
      "tool_type": "TOOL_TYPE",
      "parameters": [
        {"name": "param_name", "value": "param_value"},
        ...
      ],
      "explanation": "Why you chose this tool"
    },
    ...
  ],
  "query_analysis": "Your analysis of the user's query",
  "requires_clarification": false,
  "clarification_question": null
}

If the user's query is unclear or missing important information, set
"requires_clarification" to true and provide a clarification question.

Examples:
- For "Find restaurants near Liberty Square in Tbilisi", use GEOCODE to get coordinates
  of Liberty Square, then SEARCH_PLACES to find restaurants nearby.
- For "How far is Mtskheta from Tbilisi?", use DISTANCE_MATRIX to calculate the distance.
- For "Tell me about Fabrika in Tbilisi", use SEARCH_PLACES to find it, then PLACE_DETAILS
  to get more information.
"""
    
    async def route(self, query: UserQuery) -> RouterResponse:
        """Route a user query to the appropriate tools.
        
        Args:
            query: The user query
            
        Returns:
            Router response with selected tools
        """
        try:
            # Send the query to OpenAI's API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": query.query}
                ],
                response_format={"type": "json_object"}
            )
            
            # Extract and parse the response content
            content = response.choices[0].message.content
            router_data = json.loads(content)
            
            # Convert the raw data to our schema objects
            selected_tools = []
            for tool_data in router_data.get("selected_tools", []):
                tool_type_str = tool_data.get("tool_type", "")
                
                # Convert string tool type to enum value
                try:
                    tool_type = ToolType(tool_type_str.lower())
                except ValueError:
                    # Skip invalid tool types
                    continue
                
                # Convert parameters
                parameters = []
                for param in tool_data.get("parameters", []):
                    parameters.append(
                        ToolParameter(
                            name=param.get("name", ""),
                            value=param.get("value", "")
                        )
                    )
                
                selected_tools.append(
                    ToolCall(
                        tool_type=tool_type,
                        parameters=parameters,
                        explanation=tool_data.get("explanation", "")
                    )
                )
            
            return RouterResponse(
                selected_tools=selected_tools,
                query_analysis=router_data.get("query_analysis", ""),
                requires_clarification=router_data.get("requires_clarification", False),
                clarification_question=router_data.get("clarification_question")
            )
            
        except Exception as e:
            # In case of an error, return a response requesting clarification
            return RouterResponse(
                selected_tools=[],
                query_analysis=f"Error analyzing query: {str(e)}",
                requires_clarification=True,
                clarification_question="I'm having trouble understanding your request. Could you please rephrase it?"
            ) 