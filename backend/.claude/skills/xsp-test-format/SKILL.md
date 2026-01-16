---
name: xsp-test-format
description: Format test cases for XSP (Experience Platform) project. Use when JIRA issue starts with "XSP-". Focuses on user experience, platforms, and performance.
version: 1.0.0
---

# XSP Project Test Case Format

Generate test cases for XSP (Experience Platform) project with UX and platform focus.

## Output Format

```json
{
  "test_cases": [
    {
      "title": "User-centric test case title",
      "type": "ui-ux|api|integration|e2e",
      "priority": "high|medium|low",
      "platform": "Web|Mobile|API|All",
      "user_story": "As a [role], I want to [action], so that [benefit]",
      "preconditions": ["precondition 1", "precondition 2"],
      "steps": [
        {
          "step_number": 1,
          "action": "Action to perform",
          "expected_result": "Expected result"
        }
      ],
      "expected_outcome": "Overall expected outcome",
      "performance_criteria": {
        "page_load": "<2s",
        "api_response": "<500ms"
      },
      "platform_coverage": ["Chrome", "Firefox", "Safari"],
      "tags": ["xsp-project", "other-tags"]
    }
  ],
  "coverage_summary": "Coverage summary"
}
```

## XSP-Specific Requirements:

- Always include **platform** (Web/Mobile/API/All)
- Always include **user_story** in "As a... I want... So that..." format
- Add **performance_criteria** object with thresholds
- Add **platform_coverage** array listing browsers/devices
- Use tag `xsp-project`
- Focus on user experience and cross-platform compatibility

Generate EXACTLY 2 test cases focused on user journeys and platform compatibility.
