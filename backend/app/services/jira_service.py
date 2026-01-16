from jira import JIRA
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class JiraService:
    def __init__(self, jira_url: str, email: str, api_token: str):
        self.jira_client = JIRA(
            server=jira_url,
            basic_auth=(email, api_token)
        )

    def get_issue_details(self, issue_key: str) -> Dict:
        """
        Fetch issue details from JIRA including description and acceptance criteria.
        """
        try:
            issue = self.jira_client.issue(issue_key)

            # Extract acceptance criteria from description or custom field
            acceptance_criteria = self._extract_acceptance_criteria(issue)

            return {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description or "",
                "acceptance_criteria": acceptance_criteria,
                "issue_type": issue.fields.issuetype.name,
                "status": issue.fields.status.name,
                "priority": issue.fields.priority.name if issue.fields.priority else "Medium",
            }
        except Exception as e:
            logger.error(f"Error fetching JIRA issue {issue_key}: {str(e)}")
            raise Exception(f"Failed to fetch JIRA issue: {str(e)}")

    def _extract_acceptance_criteria(self, issue) -> List[str]:
        """
        Extract acceptance criteria from JIRA issue.
        Can be in description or a custom field.
        """
        criteria = []

        # Try to get from custom field first (common field name: customfield_xxxxx)
        # You may need to adjust this based on your JIRA configuration
        try:
            if hasattr(issue.fields, 'customfield_10100'):  # Example custom field
                ac_field = getattr(issue.fields, 'customfield_10100')
                if ac_field:
                    criteria = [ac_field] if isinstance(ac_field, str) else ac_field
        except AttributeError:
            pass

        # If not found in custom field, parse from description
        if not criteria and issue.fields.description:
            description = issue.fields.description

            # Look for acceptance criteria section
            ac_markers = [
                "acceptance criteria:",
                "ac:",
                "acceptance:",
                "criteria:",
            ]

            for marker in ac_markers:
                if marker in description.lower():
                    # Extract text after the marker
                    parts = description.lower().split(marker)
                    if len(parts) > 1:
                        ac_text = parts[1].split('\n\n')[0]  # Get until next paragraph
                        # Split by newlines and filter empty lines
                        criteria = [
                            line.strip().lstrip('*-•').strip()
                            for line in ac_text.split('\n')
                            if line.strip() and line.strip() not in ['', '*', '-', '•']
                        ]
                        break

        return criteria if criteria else ["No acceptance criteria provided"]

    def create_test_case_issue(
        self,
        project_key: str,
        test_case_summary: str,
        test_case_description: str,
        parent_issue_key: Optional[str] = None
    ) -> str:
        """
        Create a test case issue in JIRA (optional feature).
        """
        try:
            issue_dict = {
                'project': {'key': project_key},
                'summary': test_case_summary,
                'description': test_case_description,
                'issuetype': {'name': 'Test'},  # Adjust based on your JIRA setup
            }

            if parent_issue_key:
                issue_dict['parent'] = {'key': parent_issue_key}

            new_issue = self.jira_client.create_issue(fields=issue_dict)
            return new_issue.key
        except Exception as e:
            logger.error(f"Error creating test case in JIRA: {str(e)}")
            raise Exception(f"Failed to create JIRA test case: {str(e)}")
