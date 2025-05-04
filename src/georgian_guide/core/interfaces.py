"""Core interfaces for the Georgian Guide application.

This module defines the abstract interfaces for the application components.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from georgian_guide.schemas.query import (
    AssistantResponse,
    RouterResponse,
    ToolCall,
    ToolCallResult,
    UserQuery,
)


class ToolInterface(ABC):
    """Abstract interface for Google Maps MCP tools."""
    
    @abstractmethod
    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with the given parameters.
        
        Args:
            parameters: Tool parameters
            
        Returns:
            Tool execution results
        """
        pass


class RouterInterface(ABC):
    """Abstract interface for the LLM router."""
    
    @abstractmethod
    async def route(self, query: UserQuery) -> RouterResponse:
        """Route a user query to the appropriate tools.
        
        Args:
            query: The user query
            
        Returns:
            Router response with selected tools
        """
        pass


class OutputReceiverInterface(ABC):
    """Abstract interface for the output receiver."""
    
    @abstractmethod
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
        pass


class QueryProcessorInterface(ABC):
    """Abstract interface for the end-to-end query processor."""
    
    @abstractmethod
    async def process_query(self, query: UserQuery) -> AssistantResponse:
        """Process a user query end-to-end.
        
        Args:
            query: The user query
            
        Returns:
            Final assistant response
        """
        pass 