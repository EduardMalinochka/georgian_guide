"""Query schemas for the Georgian Guide application.

This module defines the schema models for user queries and assistant responses.
"""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from georgian_guide.schemas.base import ToolType


class UserQuery(BaseModel):
    """Schema representing a user query to the assistant."""
    
    query: str = Field(..., description="The natural language query from the user")
    user_id: Optional[str] = Field(None, description="Optional user identifier for personalization")
    language: Optional[str] = Field("en", description="Preferred language for responses")
    location: Optional[Dict[str, float]] = Field(
        None, 
        description="User's current location as {latitude: float, longitude: float}"
    )


class ToolParameter(BaseModel):
    """Schema representing a parameter for a tool call."""
    
    name: str = Field(..., description="Parameter name")
    value: Any = Field(..., description="Parameter value")


class ToolCall(BaseModel):
    """Schema representing a tool call recommendation."""
    
    tool_type: ToolType = Field(..., description="Type of tool to call")
    parameters: List[ToolParameter] = Field(..., description="Parameters for the tool call")
    explanation: str = Field(..., description="Explanation of why this tool is being called")


class ToolCallResult(BaseModel):
    """Schema representing the result of a tool call."""
    
    tool_type: ToolType = Field(..., description="Type of tool that was called")
    result: Dict[str, Any] = Field(..., description="Result data from the tool call")
    success: bool = Field(..., description="Whether the tool call was successful")
    error_message: Optional[str] = Field(None, description="Error message if the call failed")


class RouterResponse(BaseModel):
    """Schema representing the LLM router's response with tool selection."""
    
    selected_tools: List[ToolCall] = Field(..., description="Tools selected by the router")
    query_analysis: str = Field(..., description="Analysis of the user query")
    requires_clarification: bool = Field(False, description="Whether clarification is needed")
    clarification_question: Optional[str] = Field(
        None, 
        description="Question to ask the user for clarification"
    )


class AssistantResponse(BaseModel):
    """Schema representing the final assistant response to the user."""
    
    response: str = Field(..., description="Natural language response to the user")
    source_information: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Information sources used to generate the response"
    )
    follow_up_questions: List[str] = Field(
        default_factory=list,
        description="Suggested follow-up questions"
    ) 