import json
from dotenv import load_dotenv

from utils.csv_reader import read_recipients
from utils.context_builder import build_email_prompt
from utils.gmail_sender import send_email
from crews.drafting_crew import create_drafting_crew

load_dotenv()

CSV_PATH = "input/recipients.csv"

if __name__ == "__main__":
    recipients = read_recipients(CSV_PATH)

    for person in recipients:
        print(f"Generating email for {person['name']}...")

        prompt = build_email_prompt(
            name=person["name"],
            key_points=person["key_points"]
        )

        crew = create_drafting_crew(prompt)
        result = crew.kickoff()

        email_content = json.loads(str(result))

        send_email(
            subject=email_content["subject"],
            body=email_content["body"],
            recipients=[person["email"]]
        )

    print("All emails sent successfully.")
