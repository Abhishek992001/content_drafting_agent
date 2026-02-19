# Content Drafting Agent (CSV → Email Automation)

This project is a **production-style AI agent** built using **CrewAI** and a local LLM (**Phi-3 via Ollama**).  
It automates drafting and sending personalized emails based on structured CSV input, with a safe preview-first workflow.

---

## 🚀 What This Project Does

- Accepts a **CSV file** with recipient details
- Uses an **AI agent** to draft personalized email content
- Shows a **preview (dry run)** before sending
- Sends emails automatically via **Gmail SMTP**
- Provides real-time **UI feedback** using Streamlit

Each row in the CSV is treated independently, allowing multiple recipients and different topics in one run.

---

## 🧠 How CrewAI Is Used

- A **Content Drafting Agent** is defined with a clear role and goal
- For each CSV row, a **dynamic task** is created with contextual inputs
- A **Crew** executes the agent and task to generate structured output
- CrewAI handles the **reasoning and content generation**, while the system handles I/O and actions

---

## 🛠️ Tech Stack

- **CrewAI** – Agent orchestration
- **Phi-3 (via Ollama)** – Local LLM inference
- **Streamlit** – User interface
- **Python** – Core implementation
- **Gmail SMTP** – Email delivery

---

## 📂 Project Structure

