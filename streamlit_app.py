import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from app.utils.csv_reader import read_recipients
from app.utils.context_builder import build_email_prompt
from app.utils.gmail_sender import send_email
from app.utils.json_parser import extract_json

from app.agents.content_agent import create_content_agent
from app.agents.reviewer_agent import create_reviewer_agent
from app.tasks.drafting_task import create_drafting_task
from app.tasks.review_task import create_review_task
from crewai import Crew

# --------------------------------------------------
# Environment
# --------------------------------------------------
load_dotenv(dotenv_path=".env", override=True)

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Email Automation",
    layout="centered"
)

st.title("📧 Multi-Agent Email Automation (CrewAI)")
st.write(
    "This app uses **two AI agents**:\n"
    "- ✍️ Drafting Agent (writes the email)\n"
    "- 🔍 Reviewer Agent (approves or rejects)\n\n"
    "Emails are only sent if approved."
)

SEND_EMAILS = st.checkbox("Send emails (uncheck for dry run)", value=False)

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

# --------------------------------------------------
# Main logic
# --------------------------------------------------
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        csv_path = tmp.name

    recipients = read_recipients(csv_path)
    st.success(f"{len(recipients)} recipient(s) loaded.")

    if st.button("Generate → Review → Send"):
        progress = st.progress(0.0)

        # Create agents ONCE (important for speed)
        drafting_agent = create_content_agent()
        reviewer_agent = create_reviewer_agent()

        for idx, person in enumerate(recipients):
            st.divider()
            st.subheader(f"👤 {person['name']}")

            status = st.status("🧠 Drafting email...", expanded=False)

            try:
                # -------------------------
                # 1️⃣ Drafting
                # -------------------------
                prompt = build_email_prompt(
                    name=person["name"],
                    key_points=person["key_points"]
                )

                drafting_task = create_drafting_task(
                    drafting_agent,
                    prompt
                )

                drafting_crew = Crew(
                    agents=[drafting_agent],
                    tasks=[drafting_task],
                    verbose=False
                )

                draft_result = drafting_crew.kickoff()
                email_content = extract_json(str(draft_result))

                status.update(
                    label="🔍 Reviewing email...",
                    state="running"
                )

                # -------------------------
                # 2️⃣ Review
                # -------------------------
                review_task = create_review_task(
                    reviewer_agent,
                    email_content
                )

                review_crew = Crew(
                    agents=[reviewer_agent],
                    tasks=[review_task],
                    verbose=False
                )

                review_result = review_crew.kickoff()
                review_decision = extract_json(str(review_result))

                # -------------------------
                # 3️⃣ Decision
                # -------------------------
                if review_decision.get("approved") is True:
                    if SEND_EMAILS:
                        send_email(
                            subject=email_content["subject"],
                            body=email_content["body"],
                            recipients=[person["email"]]
                        )
                        status.update(
                            label=f"✅ Approved & sent to {person['email']}",
                            state="complete"
                        )
                    else:
                        status.update(
                            label="🟡 Approved (dry run — not sent)",
                            state="complete"
                        )
                else:
                    status.update(
                        label=f"❌ Rejected by reviewer: {review_decision.get('reason')}",
                        state="error"
                    )

                # -------------------------
                # Preview
                # -------------------------
                with st.expander("📄 Email Preview"):
                    st.markdown(f"**Subject:** {email_content['subject']}")
                    st.text(email_content["body"])

            except Exception as e:
                status.update(
                    label="❌ Error during processing",
                    state="error"
                )
                st.error("Something went wrong for this recipient.")
                st.exception(e)

            progress.progress((idx + 1) / len(recipients))

        st.success("🎉 Processing completed.")
