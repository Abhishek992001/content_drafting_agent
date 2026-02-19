def build_email_prompt(name, key_points):
    points = "\n".join([f"- {kp}" for kp in key_points])

    return f"""
Write a professional and friendly internal email.

Recipient Name: {name}

Purpose:
Announce a new internal AI tool.

Key Points:
{points}

Return ONLY valid JSON in this format:
{{
  "subject": "",
  "body": ""
}}
"""
