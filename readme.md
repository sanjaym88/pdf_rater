# Resume Rater – AI-Powered Resume Scoring App

An AI-powered web application that evaluates your resume PDF against a job description and returns a compatibility score using LLaMA-3 via the Groq API.

---

## Features

- Upload resume (PDF)
- Paste job description
- Uses LLaMA-3 (via Groq + LangChain)
- Returns a score and evaluation
- Frontend + FastAPI backend

---

## Project Structure
├── backend/
│ ├── app.py # FastAPI server
│ ├── rr2.py # AI logic with LangChain + Groq
│ ├── jd.txt # Job Description input
│ └── prompt.txt # Prompt template for LLM
├── frontend/
│ ├── index.html # Web UI
│ ├── script.js # JS logic to interact with backend
├── requirements.txt # Python dependencies
├── README.md # Project info and instructions