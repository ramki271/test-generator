# Claude Agent SDK Architecture

## Overview

This microservice uses the **Claude Agent SDK** to create an autonomous agentic system for test case generation. The agent operates without user interaction, running a complete agentic loop from requirements analysis to structured test case output.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Microservice                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐        ┌────────────────────────────────┐    │
│  │  API Routes  │───────>│  TestCaseGeneratorAgent        │    │
│  └──────────────┘        │  (Claude Agent SDK)            │    │
│                          └────────────────────────────────┘    │
│                                      │                           │
│                                      │                           │
│                          ┌───────────▼─────────────┐            │
│                          │   Agentic Loop          │            │
│                          │  ┌──────────────────┐   │            │
│                          │  │ 1. Analyze       │   │            │
│                          │  │ 2. Generate      │   │            │
│                          │  │ 3. Validate      │   │            │
│                          │  │ 4. Structure     │   │            │
│                          │  └──────────────────┘   │            │
│                          └───────────┬─────────────┘            │
│                                      │                           │
│                          ┌───────────▼─────────────┐            │
│                          │   Custom Tools (MCP)    │            │
│                          │  ┌──────────────────┐   │            │
│                          │  │ validate_test    │   │            │
│                          │  │ structure_cases  │   │            │
│                          │  │ (+ JIRA MCP*)    │   │            │
│                          │  └──────────────────┘   │            │
│                          └─────────────────────────┘            │
│                                                                   │
│  ┌──────────────┐        ┌────────────────────────────────┐    │
│  │ JIRA Service │        │  External JIRA MCP (Optional)  │    │
│  │ (Direct API) │        │  - Atlassian Remote MCP        │    │
│  └──────────────┘        │  - Custom JIRA MCP Server      │    │
│                          └────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Claude Agent SDK Integration

**File**: [app/agents/test_case_generator_agent.py](app/agents/test_case_generator_agent.py)

The agent uses:
- **Claude Agent SDK** (`claude-agent-sdk` package)
- **Model**: Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- **Mode**: Non-interactive (`accept_edits=True`)
- **Tools**: Custom SDK MCP servers (in-process)

```python
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, query, tool, create_sdk_mcp_server

# Agent runs autonomously without user prompts
agent_options = ClaudeAgentOptions(
    api_key=api_key,
    model="claude-sonnet-4-5-20250929",
    mcp_servers=[self.tools_server],
    accept_edits=True,  # Non-interactive mode
)
```

### 2. Agentic Loop

The agent autonomously executes a 4-step loop:

1. **Analyze Requirements**
   - Parses feature title, description, and acceptance criteria
   - Identifies test scenarios (happy path, edge cases, negative tests)

2. **Generate Test Cases**
   - Creates comprehensive test cases with steps
   - Covers all requested test types (functional, integration, E2E, etc.)

3. **Validate Quality**
   - Uses `validate_test_case` tool to check completeness
   - Ensures all required fields are present

4. **Structure Output**
   - Uses `structure_test_cases` tool to format results
   - Returns valid JSON with standardized schema

### 3. Custom Tools (SDK MCP Servers)

The agent has access to custom tools implemented as **SDK MCP servers** (in-process):

#### `validate_test_case`
```python
@tool("validate_test_case", "Validate a test case structure and completeness", {
    "test_case": dict
})
async def validate_test_case_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    # Validates structure, checks required fields, verifies steps exist
```

#### `structure_test_cases`
```python
@tool("structure_test_cases", "Structure raw test cases into the required JSON format", {
    "test_cases": list,
    "coverage_summary": str
})
async def structure_test_cases_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    # Formats output into standardized JSON schema
```

### 4. JIRA Integration Options

The service supports two modes for JIRA integration:

#### Option A: Direct JIRA API (Default)
- Uses `jira` Python package
- Direct API calls to JIRA
- Simpler setup, no additional servers

#### Option B: JIRA MCP Server (Optional)
- Uses Model Context Protocol
- Agent can autonomously interact with JIRA via tools
- Two implementations available:
  - **Atlassian Remote MCP Server** (official, requires OAuth)
  - **Custom JIRA MCP servers** (community-maintained)

**Configuration**: Set `ENABLE_JIRA_MCP=true` in `.env`

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ANTHROPIC_API_KEY` | Claude API key | ✅ Yes | - |
| `JIRA_URL` | JIRA instance URL | ⚠️ Conditional | - |
| `JIRA_EMAIL` | JIRA user email | ⚠️ Conditional | - |
| `JIRA_API_TOKEN` | JIRA API token | ⚠️ Conditional | - |
| `SERVICE_PORT` | Service port | No | 8000 |
| `LOG_LEVEL` | Logging level | No | INFO |
| `ENABLE_JIRA_MCP` | Use JIRA MCP server | No | false |

### MCP Configuration

**File**: [.mcp.json](.mcp.json)

Configure external MCP servers:

```json
{
  "mcpServers": {
    "atlassian-jira": {
      "transport": "sse",
      "url": "https://mcp.atlassian.com/v1/sse",
      "enabled": false
    }
  }
}
```

## API Workflow

### Request Flow

1. **Client sends request** to `/api/v1/generate-test-cases`
2. **FastAPI route** extracts requirements (from JIRA or manual input)
3. **Agent initialization** with SDK MCP tools
4. **Agentic loop starts** - agent autonomously:
   - Analyzes requirements
   - Generates test cases
   - Validates each test case
   - Structures final output
5. **Response returned** with structured test cases

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/generate-test-cases \
  -H "Content-Type: application/json" \
  -d '{
    "manual_input": {
      "title": "User Authentication",
      "description": "Users can login with email and password",
      "acceptance_criteria": [
        "User enters valid credentials",
        "System validates credentials",
        "User redirected to dashboard"
      ]
    },
    "test_types": ["functional"],
    "include_edge_cases": true,
    "include_negative_tests": true
  }'
```

### Agent Process (Autonomous)

The agent internally executes:

```
[Agent Start]
    ↓
[Analyze] "I need to generate functional test cases with edge and negative cases"
    ↓
[Generate] Creates 5 test cases covering various scenarios
    ↓
[Validate] Calls validate_test_case tool for each test case
    ↓
[Fix] Corrects any validation issues
    ↓
[Structure] Calls structure_test_cases tool
    ↓
[Complete] Returns final JSON
```

## Advantages of Agent SDK Approach

### vs. Simple LLM API Calls

| Feature | Simple API | Agent SDK |
|---------|------------|-----------|
| **Autonomy** | Single prompt/response | Multi-turn agentic loop |
| **Tool Use** | No native tools | Built-in tool calling |
| **Validation** | Manual parsing | Agent self-validates |
| **Reliability** | Prompt engineering | Structured tools + feedback |
| **Scalability** | Limited context | Agent manages context |

### Benefits for Microservices

1. **No User Interaction Needed** - Agent runs to completion autonomously
2. **Self-Correcting** - Agent validates and fixes its own output
3. **Extensible** - Easy to add new tools (JIRA, validators, etc.)
4. **Reliable** - Structured tools prevent hallucination
5. **Observable** - Agent actions can be logged and monitored

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# The agent will be available at http://localhost:8000
```

### Cloud Deployment Options

- **AWS ECS/Fargate**: Containerized, serverless compute
- **Google Cloud Run**: Auto-scaling containers
- **Azure Container Instances**: Simple container hosting
- **Kubernetes**: For larger-scale deployments

## Monitoring & Observability

The agentic loop can be monitored via:

1. **Structured Logging**
   ```python
   logger.info(f"Starting agentic loop for: {title}")
   logger.debug(f"Agent message: {message}")
   logger.info(f"Agent completed. Generated {count} test cases")
   ```

2. **Agent Metrics**
   - Number of tool calls
   - Loop iterations
   - Success/failure rates
   - Generation time

3. **Tool Execution Tracking**
   - Which tools were called
   - Tool results
   - Validation outcomes

## Future Enhancements

1. **Additional Tools**
   - Test case similarity checker
   - Automated test script generator
   - Code coverage analyzer

2. **Multi-Agent Coordination**
   - Specialized agents for different test types
   - Agent collaboration for complex features

3. **Enhanced JIRA Integration**
   - Automatically create test cases in JIRA
   - Link test cases to user stories
   - Update test execution results

4. **Learning & Optimization**
   - Track successful test case patterns
   - Improve based on feedback
   - Domain-specific customization

## References

- [Claude Agent SDK Documentation](https://docs.claude.com/en/api/agent-sdk/overview)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Atlassian Remote MCP Server](https://www.atlassian.com/blog/announcements/remote-mcp-server)
- [Building agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

## Summary

This microservice demonstrates a **fully autonomous agentic system** using the Claude Agent SDK:

✅ **Autonomous operation** - No user interaction required
✅ **Tool-equipped agent** - Custom MCP tools for validation and structuring
✅ **Self-correcting** - Agent validates and fixes its own output
✅ **Production-ready** - FastAPI microservice with Docker support
✅ **Extensible** - Easy to add new tools and capabilities
✅ **Observable** - Comprehensive logging and monitoring

The agent autonomously handles the complete workflow from requirements to structured test cases, making it ideal for CI/CD integration and automated testing pipelines.
