"""Query processor implementation for the Georgian Guide application.

This module implements the end-to-end query processing logic.
"""

from typing import Dict, List, Type

from georgian_guide.core.interfaces import (
    OutputReceiverInterface,
    QueryProcessorInterface,
    RouterInterface,
    ToolInterface,
)
from georgian_guide.schemas.base import ToolType
from georgian_guide.schemas.query import (
    AssistantResponse,
    ToolCallResult,
    UserQuery,
)


class QueryProcessor(QueryProcessorInterface):
    """Implementation of the query processor."""
    
    def __init__(
        self,
        router: RouterInterface,
        output_receiver: OutputReceiverInterface,
        tools: Dict[ToolType, ToolInterface]
    ):
        """Initialize the query processor.
        
        Args:
            router: LLM router component
            output_receiver: Output receiver component
            tools: Dictionary mapping tool types to their implementations
        """
        self.router = router
        self.output_receiver = output_receiver
        self.tools = tools
    
    async def process_query(self, query: UserQuery) -> AssistantResponse:
        """Process a user query end-to-end.
        
        Args:
            query: The user query
            
        Returns:
            Final assistant response
        """
        # Route the query to select appropriate tools
        router_response = await self.router.route(query)
        
        # If clarification is needed, return early with the clarification question
        if router_response.requires_clarification:
            return AssistantResponse(
                response=router_response.clarification_question or "Could you provide more details?",
                source_information=[],
                follow_up_questions=[]
            )
        
        # Execute all selected tools and collect results
        tool_results: List[ToolCallResult] = []
        
        for tool_call in router_response.selected_tools:
            tool_type = tool_call.tool_type
            
            if tool_type not in self.tools:
                # Skip tool if not implemented
                tool_results.append(
                    ToolCallResult(
                        tool_type=tool_type,
                        result={},
                        success=False,
                        error_message=f"Tool {tool_type} not implemented"
                    )
                )
                continue
            
            # Convert tool parameters to dictionary
            parameters = {param.name: param.value for param in tool_call.parameters}
            
            try:
                # Execute the tool
                result = await self.tools[tool_type].execute(parameters)
                
                tool_results.append(
                    ToolCallResult(
                        tool_type=tool_type,
                        result=result,
                        success=True,
                        error_message=None
                    )
                )
            except Exception as e:
                # Handle tool execution errors
                tool_results.append(
                    ToolCallResult(
                        tool_type=tool_type,
                        result={},
                        success=False,
                        error_message=str(e)
                    )
                )
        
        # Process the results to generate the final response
        return await self.output_receiver.process_results(query, tool_results) 