from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class TestCaseType(str, Enum):
    FUNCTIONAL = "functional"
    INTEGRATION = "integration"
    E2E = "e2e"
    UNIT = "unit"
    API = "api"


class TestCasePriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class JiraIssueInput(BaseModel):
    issue_key: str = Field(..., description="JIRA issue key (e.g., PROJ-123)")


class ManualInput(BaseModel):
    title: str = Field(..., description="Feature/Story title")
    description: str = Field(..., description="Detailed description")
    acceptance_criteria: List[str] = Field(..., description="List of acceptance criteria")


class TestCaseGenerationRequest(BaseModel):
    jira_issue: Optional[JiraIssueInput] = None
    manual_input: Optional[ManualInput] = None
    test_types: List[TestCaseType] = Field(
        default=[TestCaseType.FUNCTIONAL],
        description="Types of test cases to generate"
    )
    include_edge_cases: bool = Field(default=True, description="Include edge case scenarios")
    include_negative_tests: bool = Field(default=True, description="Include negative test scenarios")


class TestStep(BaseModel):
    step_number: int
    action: str
    expected_result: str


class TestCase(BaseModel):
    title: str
    description: str
    type: TestCaseType
    priority: TestCasePriority
    preconditions: List[str]
    steps: List[TestStep]
    expected_outcome: str
    tags: List[str]


class TestCaseGenerationResponse(BaseModel):
    issue_key: Optional[str] = None
    feature_title: str
    test_cases: List[TestCase]
    coverage_summary: str
    generation_metadata: dict


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
