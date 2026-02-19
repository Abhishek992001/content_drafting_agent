from crewai import Task

def create_review_task(agent, email_content):
    return Task(
        description=f"""
Review the following email content.

Subject:
{email_content['subject']}

Body:
{email_content['body']}

Decide if this email is safe and appropriate to send.

Return ONLY valid JSON:
{{
  "approved": true or false,
  "reason": ""
}}
""",
        expected_output="JSON with approval decision",
        agent=agent
    )
