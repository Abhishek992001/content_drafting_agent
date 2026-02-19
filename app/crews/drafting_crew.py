from crewai import Crew
from app.agents.content_agent import create_content_agent
from app.agents.reviewer_agent import create_reviewer_agent
from app.tasks.drafting_task import create_drafting_task
from app.tasks.review_task import create_review_task

def create_drafting_and_review_crew(prompt, drafted_email=None):
    drafting_agent = create_content_agent()
    reviewer_agent = create_reviewer_agent()

    tasks = []

    # Drafting task
    tasks.append(create_drafting_task(drafting_agent, prompt))

    # Review task (runs after drafting)
    if drafted_email:
        tasks.append(create_review_task(reviewer_agent, drafted_email))

    return Crew(
        agents=[drafting_agent, reviewer_agent],
        tasks=tasks,
        verbose=False
    )
