# Test Case Generator Service

A Python FastAPI microservice that generates comprehensive test cases from JIRA acceptance criteria using **Claude Agent SDK** with autonomous agentic workflows.

> 🤖 **Powered by Claude Agent SDK** - This service uses an autonomous agent that runs a complete agentic loop to generate, validate, and structure test cases without user interaction.

## Features

### Agentic Capabilities
- **🤖 Autonomous Agent**: Uses Claude Agent SDK for self-directed test case generation
- **🔧 Custom Tools**: Built-in MCP tools for validation and structuring
- **🔄 Self-Correcting**: Agent validates and fixes its own output
- **📊 Structured Output**: Guaranteed valid JSON response format

### Integration & Testing
- **JIRA Integration**: Automatically fetch user stories, descriptions, and acceptance criteria from JIRA
- **Manual Input Support**: Generate test cases without JIRA by providing details directly
- **MCP Support**: Optional JIRA MCP server integration for advanced tool use
- **Multiple Test Types**: Support for functional, integration, E2E, unit, and API tests
- **Comprehensive Coverage**: Includes positive, negative, and edge case scenarios

### Deployment
- **RESTful API**: Easy integration with CI/CD pipelines and other tools
- **Docker Support**: Containerized deployment with Docker and docker-compose
- **Non-Interactive**: Fully autonomous - no user prompts required
- **Production Ready**: Built on FastAPI with async support

## Architecture

```
test-case-generator-service/
├── app/
│   ├── agents/
│   │   └── test_case_generator_agent.py  # Claude Agent for test generation
│   ├── api/
│   │   └── routes.py                      # FastAPI endpoints
│   ├── models/
│   │   └── schemas.py                     # Pydantic models
│   ├── services/
│   │   └── jira_service.py                # JIRA integration
│   ├── config.py                          # Configuration management
│   └── main.py                            # FastAPI application
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## How It Works

The service uses an **autonomous agentic loop** powered by Claude Agent SDK:

1. **Receive Request** - API receives requirements (from JIRA or manual input)
2. **Agent Initialization** - Agent equipped with custom MCP tools
3. **Agentic Loop** - Agent autonomously:
   - Analyzes requirements and acceptance criteria
   - Generates comprehensive test cases
   - Validates each test case using tools
   - Structures output in required format
4. **Return Results** - Structured test cases sent back to client

See [CLAUDE_AGENT_SDK_ARCHITECTURE.md](CLAUDE_AGENT_SDK_ARCHITECTURE.md) for detailed architecture documentation.

## Prerequisites

- Python 3.10+ (required for Claude Agent SDK)
- Docker (optional)
- Anthropic API key
- JIRA account with API token (if using JIRA integration)

## Setup

### 1. Clone and Install Dependencies

```bash
cd test-case-generator-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token
SERVICE_PORT=8000
LOG_LEVEL=INFO
```

### 3. Run the Service

#### Using Python directly:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Using Docker:
```bash
docker-compose up --build
```

## API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### Generate Test Cases from JIRA
```bash
POST /api/v1/generate-test-cases
Content-Type: application/json

{
  "jira_issue": {
    "issue_key": "PROJ-123"
  },
  "test_types": ["functional", "integration"],
  "include_edge_cases": true,
  "include_negative_tests": true
}
```

### Generate Test Cases from Manual Input
```bash
POST /api/v1/generate-test-cases
Content-Type: application/json

{
  "manual_input": {
    "title": "User Login Feature",
    "description": "Users should be able to login using email and password",
    "acceptance_criteria": [
      "User can enter email and password",
      "System validates credentials",
      "User is redirected to dashboard on success",
      "Error message shown on invalid credentials"
    ]
  },
  "test_types": ["functional", "api"],
  "include_edge_cases": true,
  "include_negative_tests": true
}
```

### Get JIRA Issue Details
```bash
GET /api/v1/jira/issue/{issue_key}
```

## Example Response

```json
{
  "issue_key": "PROJ-123",
  "feature_title": "User Login Feature",
  "test_cases": [
    {
      "title": "Successful login with valid credentials",
      "description": "Verify user can login with correct email and password",
      "type": "functional",
      "priority": "high",
      "preconditions": [
        "User account exists",
        "Application is accessible"
      ],
      "steps": [
        {
          "step_number": 1,
          "action": "Navigate to login page",
          "expected_result": "Login form is displayed"
        },
        {
          "step_number": 2,
          "action": "Enter valid email address",
          "expected_result": "Email is accepted"
        },
        {
          "step_number": 3,
          "action": "Enter valid password",
          "expected_result": "Password is masked"
        },
        {
          "step_number": 4,
          "action": "Click login button",
          "expected_result": "User is authenticated and redirected to dashboard"
        }
      ],
      "expected_outcome": "User successfully logs in and lands on dashboard",
      "tags": ["authentication", "happy-path"]
    }
  ],
  "coverage_summary": "Generated 8 test cases covering happy path, edge cases, and negative scenarios",
  "generation_metadata": {
    "test_types_requested": ["functional", "api"],
    "include_edge_cases": true,
    "include_negative_tests": true,
    "total_test_cases_generated": 8
  }
}
```

## Usage Examples

### Using cURL

```bash
# Generate test cases from JIRA
curl -X POST http://localhost:8000/api/v1/generate-test-cases \
  -H "Content-Type: application/json" \
  -d '{
    "jira_issue": {"issue_key": "PROJ-123"},
    "test_types": ["functional"],
    "include_edge_cases": true,
    "include_negative_tests": true
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/api/v1/generate-test-cases"
payload = {
    "manual_input": {
        "title": "Payment Processing",
        "description": "Process credit card payments",
        "acceptance_criteria": [
            "Accept credit card details",
            "Validate card information",
            "Process payment through gateway",
            "Show confirmation on success"
        ]
    },
    "test_types": ["functional", "integration"],
    "include_edge_cases": True,
    "include_negative_tests": True
}

response = requests.post(url, json=payload)
test_cases = response.json()
print(f"Generated {len(test_cases['test_cases'])} test cases")
```

## Integration with CI/CD

You can integrate this service into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Generate Test Cases
  run: |
    response=$(curl -X POST http://test-generator:8000/api/v1/generate-test-cases \
      -H "Content-Type: application/json" \
      -d '{"jira_issue": {"issue_key": "${{ env.JIRA_ISSUE }}"}}')
    echo "$response" > test-cases.json
```

## Configuration Options

| Environment Variable | Description | Required | Default |
|---------------------|-------------|----------|---------|
| ANTHROPIC_API_KEY | Anthropic API key | Yes | - |
| JIRA_URL | JIRA instance URL | Yes* | - |
| JIRA_EMAIL | JIRA user email | Yes* | - |
| JIRA_API_TOKEN | JIRA API token | Yes* | - |
| SERVICE_PORT | Service port | No | 8000 |
| LOG_LEVEL | Logging level | No | INFO |
| ENABLE_JIRA_MCP | Use JIRA MCP server | No | false |

*Required only if using JIRA integration

## Claude Agent SDK Details

This service uses the **Claude Agent SDK** to create an autonomous agent that:

- **Runs without user interaction** - Agent executes a complete workflow autonomously
- **Uses custom tools** - In-process MCP tools for validation and structuring
- **Self-validates** - Agent checks and corrects its own output
- **Handles complexity** - Multi-turn agentic loop for comprehensive test generation

### Agent Tools

The agent has access to these custom tools:

1. **`validate_test_case`** - Validates test case structure and completeness
2. **`structure_test_cases`** - Formats output into required JSON schema
3. **JIRA MCP** (optional) - Direct tool-based JIRA integration

### Agent SDK vs. Simple API

| Aspect | Simple LLM API | Agent SDK (This Service) |
|--------|----------------|--------------------------|
| Operation | Single request/response | Autonomous multi-turn loop |
| Tools | None | Built-in MCP tools |
| Validation | Manual | Agent self-validates |
| Reliability | Prompt-dependent | Tool-enforced structure |
| Extensibility | Limited | Easy to add new tools |

## Getting JIRA API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label and copy the token
4. Use this token in your `.env` file

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

## Troubleshooting

### JIRA Connection Issues
- Verify your JIRA URL is correct (include https://)
- Ensure API token is valid and not expired
- Check that your JIRA user has permission to access the issues

### Claude API Issues
- Verify your Anthropic API key is valid
- Check API usage limits
- Ensure you have access to Claude Sonnet 4.5

### Service Not Starting
- Check all required environment variables are set
- Verify port 8000 is not already in use
- Check logs for detailed error messages

## License

MIT

## Support

For issues and questions, please open an issue in the repository.
