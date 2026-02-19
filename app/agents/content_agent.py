from crewai import Agent
from app.config.llm_config import llm


def create_content_agent():
    return Agent(
        role="Content Drafting Specialist",
        goal="Draft a clear,concise and professional content",
        backstory=("you are an expert content writer skilled in emails,Marketing descriptions and internal documentation"),
        llm=llm,
        verbose=True
    )