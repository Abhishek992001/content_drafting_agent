from crewai import Agent
from app.config.llm_config import llm

def create_reviewer_agent():
    return Agent(
        role="Content Quality Reviewer",
        goal="Review drafted email content and ensure it is clear, professional, and safe to send",
        backstory=(
            "You are a senior editor responsible for reviewing internal communications. "
            "You ensure emails are appropriate, professional, and free of errors."
        ),
        llm=llm,
        verbose=False
    )
