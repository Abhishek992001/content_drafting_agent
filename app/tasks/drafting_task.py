from crewai import Task

def create_drafting_task(agent, prompt):
    return Task(
        description=prompt,
        expected_output="Strict JSON with subject and body",
        agent=agent
    )
