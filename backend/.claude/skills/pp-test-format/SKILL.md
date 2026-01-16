---
name: pp-test-format
description: Format test cases for PP (Priority Program) project. Use when JIRA issue starts with "PP-". Focuses on business impact, data validation, and compliance.
version: 1.0.0
---

# PP Project Test Case Format

Generate test cases for PP (Priority Program) project with business-focused additions.

## Output Format

```json
{
  "test_cases": [
    {
      "title": "Clear test case title",
      "type": "functional|integration|performance|data-validation",
      "priority": "high|medium|low",
      "business_impact": "Critical|High|Medium|Low",
      "data_volume": "Small|Medium|Large",
      "preconditions": ["precondition 1", "precondition 2"],
      "steps": [
        {
          "step_number": 1,
          "action": "Action to perform",
          "expected_result": "Expected result"
        }
      ],
      "expected_outcome": "Overall expected outcome",
      "compliance_requirements": ["HIPAA items if applicable"],
      "tags": ["pp-project", "other-tags"]
    }
  ],
  "coverage_summary": "Coverage summary"
}
```

## PP-Specific Requirements:

- Always include **business_impact** (Critical/High/Medium/Low)
- Always include **data_volume** (Small/Medium/Large)
- Add **compliance_requirements** array when relevant (HIPAA, PHI, audit)
- Use tag `pp-project`
- Focus on data accuracy and business value

Generate EXACTLY 2 test cases focused on business value and data validation.
