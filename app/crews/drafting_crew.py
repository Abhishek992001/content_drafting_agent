from crewai import Crew
from app.agents.content_agent import create_content_agent
from app.tasks.drafting_task import create_drafting_task

def create_drafting_crew(prompt):
    agent = create_content_agent()
    task = create_drafting_task(agent, prompt)

    return Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )
