"""Output receiver implementation for the Georgian Guide application.

This module implements the output receiver that processes tool results and
generates the final response.
"""

import json
import os
from typing import Any, Dict, List

import openai
from openai import OpenAI

from georgian_guide.core.interfaces import OutputReceiverInterface
from georgian_guide.schemas.query import AssistantResponse, ToolCallResult, UserQuery


class OpenAIOutputReceiver(OutputReceiverInterface):
    """Output receiver implementation using OpenAI's API."""
    
    def __init__(self, model: str = "gpt-4o"):
        """Initialize the output receiver.
        
        Args:
            model: The OpenAI model to use for response generation
        """
        self.model = model
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Define the system message that instructs the LLM on how to format responses
        self.system_message = """
You are an AI assistant for travelers in Georgia (the country). Your job is to help
users find places to visit, restaurants, attractions, and other points of interest.

You have access to information from Google Maps tools. I will provide you with:
1. The user's original query
2. The results from various Google Maps tools that were called to answer the query

Create a helpful, informative response for the user based on this information.
Your response should be:
- Natural and conversational
- Directly addressing the user's query
- Incorporating the information from the tool results
- Providing specific details about places (location, ratings, etc. when available)
- Culturally aware of Georgian customs and traditions

If tool calls failed or returned no results, mention this briefly and suggest
alternatives or ask for clarification if needed.

Also suggest 1-3 relevant follow-up questions the user might want to ask.

YOUR RESPONSE MUST BE VALID JSON in the following format:
{
  "response": "Your helpful response to the user",
  "source_information": [
    {"type": "Place", "name": "Place Name", "details": "Brief summary of details used"}
  ],
  "follow_up_questions": [
    "Suggested follow-up question 1?",
    "Suggested follow-up question 2?",
    "Suggested follow-up question 3?"
  ]
}
"""
    
    async def process_results(
        self, 
        query: UserQuery, 
        tool_results: List[ToolCallResult]
    ) -> AssistantResponse:
        """Process tool results to generate the final response.
        
        Args:
            query: The original user query
            tool_results: Results from tool executions
            
        Returns:
            Final assistant response
        """
        try:
            # Format the tool results for the LLM
            formatted_results = []
            
            for result in tool_results:
                formatted_results.append({
                    "tool_type": result.tool_type.value,
                    "success": result.success,
                    "result": result.result,
                    "error_message": result.error_message
                })
            
            # Create the user message with query and results
            user_message = f"""
User Query: {query.query}

Tool Results:
{json.dumps(formatted_results, indent=2)}

Please generate a response based on this information.
"""
            
            # Send to OpenAI's API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": user_message}
                ],
                response_format={"type": "json_object"}
            )
            
            # Extract and parse the response content
            content = response.choices[0].message.content
            response_data = json.loads(content)
            
            return AssistantResponse(
                response=response_data.get("response", "Sorry, I couldn't generate a proper response."),
                source_information=response_data.get("source_information", []),
                follow_up_questions=response_data.get("follow_up_questions", [])
            )
            
        except Exception as e:
            # In case of an error, return a basic error response
            return AssistantResponse(
                response=f"I apologize, but I encountered an error while processing your request: {str(e)}. Could you please try again?",
                source_information=[],
                follow_up_questions=[]
            ) 