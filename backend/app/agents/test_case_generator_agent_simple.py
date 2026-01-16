"""
Simplified Test Case Generator using Claude API directly (fallback)
"""

from anthropic import Anthropic
from typing import List, Dict
import json
import logging
import os

logger = logging.getLogger(__name__)


class TestCaseGeneratorAgent:
    """
    Simplified test case generator using direct Anthropic API.
    This is a fallback while we debug the Claude Agent SDK integration.
    """

    def __init__(self, api_key: str, jira_service=None, jira_mcp_enabled: bool = False):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-5-20250929"
        self.jira_service = jira_service

    async def generate_test_cases(
        self,
        title: str,
        description: str,
        acceptance_criteria: List[str],
        test_types: List[str],
        include_edge_cases: bool = True,
        include_negative_tests: bool = True,
        jira_issue_key: str = None,
    ) -> Dict:
        """
        Generate test cases using Claude (direct API for now).
        """
        prompt = self._build_prompt(
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
            test_types=test_types,
            include_edge_cases=include_edge_cases,
            include_negative_tests=include_negative_tests,
        )

        try:
            logger.info(f"Generating test cases for: {title}")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                temperature=0.7,
                system=self._get_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            result = self._parse_response(response.content[0].text)
            logger.info(f"Generated {len(result.get('test_cases', []))} test cases")
            return result

        except Exception as e:
            logger.error(f"Error generating test cases: {str(e)}")
            raise Exception(f"Failed to generate test cases: {str(e)}")

    def _get_system_prompt(self) -> str:
        return """You are an expert QA engineer and test case designer. Your role is to generate comprehensive, well-structured test cases based on feature descriptions and acceptance criteria.

Your test cases should be:
1. Clear and unambiguous
2. Follow a step-by-step format
3. Cover positive, negative, and edge case scenarios
4. Include proper preconditions and expected outcomes
5. Be realistic and executable

Always return your response as a valid JSON object with the following structure:
{
  "test_cases": [
    {
      "title": "Test case title",
      "description": "Brief description",
      "type": "functional|integration|e2e|unit|api",
      "priority": "high|medium|low",
      "preconditions": ["precondition 1", "precondition 2"],
      "steps": [
        {
          "step_number": 1,
          "action": "Action to perform",
          "expected_result": "What should happen"
        }
      ],
      "expected_outcome": "Overall expected outcome",
      "tags": ["tag1", "tag2"]
    }
  ],
  "coverage_summary": "Summary of what scenarios are covered"
}"""

    def _build_prompt(
        self,
        title: str,
        description: str,
        acceptance_criteria: List[str],
        test_types: List[str],
        include_edge_cases: bool,
        include_negative_tests: bool,
    ) -> str:
        criteria_text = "\n".join([f"- {ac}" for ac in acceptance_criteria])
        test_types_text = ", ".join(test_types)

        prompt = f"""Generate comprehensive test cases for the following feature:

**Feature Title:** {title}

**Description:**
{description}

**Acceptance Criteria:**
{criteria_text}

**Requirements:**
- Generate {test_types_text} test cases
- Include edge cases: {"Yes" if include_edge_cases else "No"}
- Include negative test scenarios: {"Yes" if include_negative_tests else "No"}

Please analyze the feature and acceptance criteria carefully, then generate a complete set of test cases that ensure thorough coverage. Consider:
1. Happy path scenarios
2. Boundary conditions
3. Error handling
4. Data validation
5. User workflows

Return the test cases in the JSON format specified in your system prompt. Generate at least 5 test cases."""

        return prompt

    def _parse_response(self, response_text: str) -> Dict:
        """Parse Claude's response and extract test cases."""
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")

            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)

            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return {
                "test_cases": [],
                "coverage_summary": "Failed to parse response",
                "error": str(e)
            }
