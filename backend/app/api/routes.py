from fastapi import APIRouter, HTTPException, Depends
from app.models import (
    TestCaseGenerationRequest,
    TestCaseGenerationResponse,
    TestCase,
    TestStep,
    TestCasePriority,
    HealthResponse,
)
from app.services import JiraService
from app.agents import TestCaseGeneratorAgent
from app.config import get_settings, Settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_jira_service(settings: Settings = Depends(get_settings)) -> JiraService:
    return JiraService(
        jira_url=settings.jira_url,
        email=settings.jira_email,
        api_token=settings.jira_api_token,
    )


def get_agent(settings: Settings = Depends(get_settings), jira_service: JiraService = Depends(get_jira_service)) -> TestCaseGeneratorAgent:
    return TestCaseGeneratorAgent(
        api_key=settings.anthropic_api_key,
        jira_service=jira_service,
        jira_mcp_enabled=settings.enable_jira_mcp
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="test-case-generator",
        version="1.0.0"
    )


@router.post("/generate-test-cases", response_model=TestCaseGenerationResponse)
async def generate_test_cases(
    request: TestCaseGenerationRequest,
    jira_service: JiraService = Depends(get_jira_service),
    agent: TestCaseGeneratorAgent = Depends(get_agent),
):
    """
    Generate test cases from JIRA issue or manual input using Claude Agent SDK.
    The agent will autonomously run an agentic loop to generate comprehensive test cases.
    """
    try:
        # Determine input source
        if request.jira_issue:
            # Fetch from JIRA
            logger.info(f"Fetching JIRA issue: {request.jira_issue.issue_key}")
            jira_details = jira_service.get_issue_details(request.jira_issue.issue_key)

            title = jira_details["summary"]
            description = jira_details["description"]
            acceptance_criteria = jira_details["acceptance_criteria"]
            issue_key = jira_details["key"]

        elif request.manual_input:
            # Use manual input
            logger.info("Using manual input for test case generation")
            title = request.manual_input.title
            description = request.manual_input.description
            acceptance_criteria = request.manual_input.acceptance_criteria
            issue_key = None

        else:
            raise HTTPException(
                status_code=400,
                detail="Either jira_issue or manual_input must be provided"
            )

        # Generate test cases using the agentic loop (async)
        logger.info(f"Starting agentic loop for: {title}")
        test_types = [t.value for t in request.test_types]

        result = await agent.generate_test_cases(
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
            test_types=test_types,
            include_edge_cases=request.include_edge_cases,
            include_negative_tests=request.include_negative_tests,
            jira_issue_key=issue_key,
        )

        # Parse and structure the response
        test_cases = []
        for tc in result.get("test_cases", []):
            test_case = TestCase(
                title=tc["title"],
                description=tc["description"],
                type=tc["type"],
                priority=tc["priority"],
                preconditions=tc.get("preconditions", []),
                steps=[
                    TestStep(
                        step_number=step["step_number"],
                        action=step["action"],
                        expected_result=step["expected_result"]
                    )
                    for step in tc.get("steps", [])
                ],
                expected_outcome=tc.get("expected_outcome", ""),
                tags=tc.get("tags", []),
            )
            test_cases.append(test_case)

        response = TestCaseGenerationResponse(
            issue_key=issue_key,
            feature_title=title,
            test_cases=test_cases,
            coverage_summary=result.get("coverage_summary", ""),
            generation_metadata={
                "test_types_requested": test_types,
                "include_edge_cases": request.include_edge_cases,
                "include_negative_tests": request.include_negative_tests,
                "total_test_cases_generated": len(test_cases),
            }
        )

        logger.info(f"Successfully generated {len(test_cases)} test cases")
        return response

    except Exception as e:
        logger.error(f"Error in generate_test_cases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jira/issue/{issue_key}")
async def get_jira_issue(
    issue_key: str,
    jira_service: JiraService = Depends(get_jira_service),
):
    """
    Fetch JIRA issue details (for debugging/testing).
    """
    try:
        details = jira_service.get_issue_details(issue_key)
        return details
    except Exception as e:
        logger.error(f"Error fetching JIRA issue: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
