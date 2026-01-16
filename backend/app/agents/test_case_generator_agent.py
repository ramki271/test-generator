"""
Test Case Generator Agent using Claude Agent SDK.

This agent uses the Claude Agent SDK to autonomously generate test cases
with an agentic loop that can use tools for validation and structured output generation.
"""

from claude_agent_sdk import ClaudeAgentOptions, query, tool, create_sdk_mcp_server, AssistantMessage, TextBlock
from typing import List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


# Define custom tools as SDK MCP servers (in-process)

@tool("validate_test_case", "Validate a test case structure and completeness", {
    "test_case": dict
})
async def validate_test_case_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to validate test case structure before finalizing.
    """
    test_case = args.get("test_case", {})

    required_fields = ["title", "description", "type", "priority", "steps", "expected_outcome"]
    missing_fields = [field for field in required_fields if field not in test_case or not test_case[field]]

    validation_result = {
        "valid": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "has_steps": len(test_case.get("steps", [])) > 0,
        "has_preconditions": len(test_case.get("preconditions", [])) > 0
    }

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(validation_result, indent=2)
        }]
    }


@tool("structure_test_cases", "Structure raw test cases into the required JSON format", {
    "test_cases": list,
    "coverage_summary": str
})
async def structure_test_cases_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to help structure test cases into the required output format.
    """
    test_cases = args.get("test_cases", [])
    coverage_summary = args.get("coverage_summary", "")

    structured_output = {
        "test_cases": test_cases,
        "coverage_summary": coverage_summary,
        "total_count": len(test_cases)
    }

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(structured_output, indent=2)
        }]
    }


class TestCaseGeneratorAgent:
    """
    Agentic test case generator using Claude Agent SDK.

    This agent autonomously:
    1. Analyzes acceptance criteria
    2. Generates comprehensive test cases
    3. Validates test case quality
    4. Structures output in required format
    """

    def __init__(
        self,
        api_key: str,
        jira_service: Optional[Any] = None,
        jira_mcp_enabled: bool = False
    ):
        self.api_key = api_key
        self.jira_service = jira_service
        self.jira_mcp_enabled = jira_mcp_enabled

        # Create SDK MCP server with custom tools
        self.tools_server = create_sdk_mcp_server(
            name="test-case-tools",
            version="1.0.0",
            tools=[
                validate_test_case_tool,
                structure_test_cases_tool
            ]
        )

        # Note: API key must be set in ANTHROPIC_API_KEY environment variable
        # Configure agent options
        self.agent_options = ClaudeAgentOptions(
            model="claude-sonnet-4-5-20250929",
            mcp_servers={
                "test-case-tools": self.tools_server
            },
            permission_mode="acceptEdits",  # Non-interactive mode - auto-approve operations
            max_turns=10,  # Allow up to 10 turns for the agentic loop
            cli_path="/Users/ramakrishnan.sridar/.local/bin/claude",  # Explicit CLI path
        )

    async def generate_test_cases(
        self,
        title: str,
        description: str,
        acceptance_criteria: List[str],
        test_types: List[str],
        include_edge_cases: bool = True,
        include_negative_tests: bool = True,
        jira_issue_key: Optional[str] = None,
    ) -> Dict:
        """
        Generate test cases using the agentic loop.

        The agent will autonomously:
        - Analyze requirements
        - Generate comprehensive test cases
        - Validate each test case
        - Structure the final output
        """

        # Build the agent's task prompt
        task_prompt = self._build_agent_task(
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
            test_types=test_types,
            include_edge_cases=include_edge_cases,
            include_negative_tests=include_negative_tests,
            jira_issue_key=jira_issue_key,
        )

        try:
            logger.info(f"Starting agentic loop for test case generation: {title}")

            # Execute the agent query - this runs the full agentic loop
            # NOTE: Using async generator instead of string due to SDK bug with MCP servers
            # See: https://github.com/anthropics/claude-agent-sdk-python/issues/266
            async def generate_prompt():
                yield {
                    "type": "user",
                    "message": {
                        "role": "user",
                        "content": task_prompt
                    }
                }

            result_text = ""

            async for message in query(prompt=generate_prompt(), options=self.agent_options):
                # Process different message types
                if isinstance(message, AssistantMessage):
                    # Extract text from assistant messages
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            result_text += block.text + "\n"
                            logger.debug(f"Agent response: {block.text[:200]}...")
                # You can also handle other message types like ToolUse, ToolResult, etc.
                logger.debug(f"Message type: {type(message).__name__}")

            # Parse the final result
            parsed_result = self._parse_agent_result(result_text)

            logger.info(f"Agent completed. Generated {len(parsed_result.get('test_cases', []))} test cases")
            return parsed_result

        except Exception as e:
            logger.error(f"Error in agentic loop: {str(e)}", exc_info=True)
            raise Exception(f"Agent failed to generate test cases: {str(e)}")

    def _build_agent_task(
        self,
        title: str,
        description: str,
        acceptance_criteria: List[str],
        test_types: List[str],
        include_edge_cases: bool,
        include_negative_tests: bool,
        jira_issue_key: Optional[str] = None,
    ) -> str:
        """
        Build the agent's task prompt with clear instructions for autonomous execution.
        """
        criteria_text = "\n".join([f"- {ac}" for ac in acceptance_criteria])
        test_types_text = ", ".join(test_types)

        task = f"""You are an expert QA engineer and test case designer. Generate comprehensive test cases for the following feature.

**Feature Title:** {title}

**Description:**
{description}

**Acceptance Criteria:**
{criteria_text}

**Requirements:**
- Generate {test_types_text} test cases
- Include edge cases: {"Yes" if include_edge_cases else "No"}
- Include negative test scenarios: {"Yes" if include_negative_tests else "No"}

**Output Format - Return ONLY valid JSON:**
{{
  "test_cases": [
    {{
      "title": "Clear, descriptive test case title",
      "description": "Brief description of what is being tested",
      "type": "{test_types[0] if test_types else 'functional'}",
      "priority": "high|medium|low",
      "preconditions": ["precondition 1", "precondition 2"],
      "steps": [
        {{
          "step_number": 1,
          "action": "What to do",
          "expected_result": "What should happen"
        }}
      ],
      "expected_outcome": "Overall expected outcome",
      "tags": ["tag1", "tag2"]
    }}
  ],
  "coverage_summary": "Summary of what scenarios are covered"
}}

**Instructions:**
1. Analyze the feature and acceptance criteria
2. Generate at least 5 comprehensive test cases covering:
   - Happy path scenarios
   - {"Boundary conditions and edge cases" if include_edge_cases else "Standard cases"}
   - {"Error handling and negative scenarios" if include_negative_tests else "Positive scenarios"}
3. Ensure each test case has all required fields
4. Return ONLY the JSON object, no additional text

Begin generating test cases now."""

        return task

    def _parse_agent_result(self, result_text: str) -> Dict:
        """
        Parse the agent's final output and extract structured test cases.
        """
        try:
            # Try to find JSON in the result
            start_idx = result_text.find('{')
            end_idx = result_text.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                logger.warning("No JSON found in direct output")
                return {
                    "test_cases": [],
                    "coverage_summary": "Agent completed but no structured output found",
                    "raw_output": result_text[:500]
                }

            json_str = result_text[start_idx:end_idx]
            result = json.loads(json_str)

            # Validate the structure
            if "test_cases" not in result:
                result = {"test_cases": [], "coverage_summary": "Invalid structure"}

            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse agent output as JSON: {str(e)}")
            logger.debug(f"Result text: {result_text[:500]}...")

            return {
                "test_cases": [],
                "coverage_summary": "Failed to parse agent output",
                "error": str(e),
                "raw_output": result_text[:1000]
            }


# Helper function to create agent with JIRA integration
def create_test_case_agent(
    api_key: str,
    jira_service: Optional[Any] = None,
    jira_mcp_enabled: bool = False
) -> TestCaseGeneratorAgent:
    """
    Factory function to create a configured test case generator agent.
    """
    return TestCaseGeneratorAgent(
        api_key=api_key,
        jira_service=jira_service,
        jira_mcp_enabled=jira_mcp_enabled
    )
