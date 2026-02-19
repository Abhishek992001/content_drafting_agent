import json
import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from app.utils.csv_reader import read_recipients
from app.utils.context_builder import build_email_prompt
from app.utils.gmail_sender import send_email
from app.utils.json_parser import extract_json
from app.crews.drafting_crew import create_drafting_crew

# --------------------------------------------------
# Environment setup
# --------------------------------------------------
load_dotenv(dotenv_path=".env", override=True)

# --------------------------------------------------
# Streamlit UI setup
# --------------------------------------------------
st.set_page_config(page_title="CSV → Email Automation Agent", layout="centered")

st.title("📧 CSV to Email Automation Agent")
st.write(
    "Upload a CSV file with recipient details. "
    "The AI agent will draft personalized emails and send them automatically."
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
    # Save uploaded CSV to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        csv_path = tmp.name

    recipients = read_recipients(csv_path)
    st.success(f"{len(recipients)} recipient(s) loaded from CSV.")

    if st.button("Generate and Process Emails"):
        progress = st.progress(0.0)

        for idx, person in enumerate(recipients):
            st.write(f"### Processing: {person['name']}")

            status = st.status("🧠 Drafting email with AI...", expanded=False)

            try:
                # Build prompt for this recipient
                prompt = build_email_prompt(
                    name=person["name"],
                    key_points=person["key_points"]
                )

                # Run CrewAI agent
                crew = create_drafting_crew(prompt)
                result = crew.kickoff()

                # Safely extract JSON from agent output
                email_content = extract_json(str(result))

                status.update(label="✉️ Sending email via Gmail...", state="running")

                # Send email if enabled
                if SEND_EMAILS:
                    send_email(
                        subject=email_content["subject"],
                        body=email_content["body"],
                        recipients=[person["email"]]
                    )
                    status.update(
                        label=f"✅ Email sent to {person['email']}",
                        state="complete"
                    )
                else:
                    status.update(
                        label="🟡 Dry run — email not sent",
                        state="complete"
                    )

                # Show preview in UI
                with st.expander("📄 Email Preview"):
                    st.subheader(email_content["subject"])
                    st.text(email_content["body"])

            except Exception as e:
                status.update(
                    label=f"❌ Failed for {person['email']}",
                    state="error"
                )
                st.error("Error while processing this recipient.")
                st.text("Raw agent output:")
                st.text(str(result) if "result" in locals() else "No output")
                st.exception(e)

            progress.progress((idx + 1) / len(recipients))

        st.success("🎉 Processing completed for all recipients.")
