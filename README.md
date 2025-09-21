<<<<<<< HEAD
# Automated Resume Relevance Check System\n\nProject README content here.
# 📄 Automated Resume Relevance Check System

## Project Overview
The **Automated Resume Relevance Check System** is an AI-driven platform designed to streamline the resume evaluation process. It automatically compares resumes against job descriptions, generating a **relevance score (0–100)** for each candidate. The system highlights missing skills, certifications, or projects, and provides **AI-driven improvement suggestions**. It supports both **single and bulk resume evaluation**, ranks top candidates for each job role, and ensures fast, consistent, and data-driven shortlisting, reducing manual workload for placement teams.

---

## Features

### Single Resume Evaluation
- Upload one resume and one job description (PDF/DOCX)  
- Generate a **Relevance Score**  
- Identify missing skills, certifications, and projects  
- Receive **AI-generated improvement suggestions**  
- Verdict: **High / Medium / Low suitability**

### Bulk Resume Evaluation
- Upload multiple resumes and multiple job descriptions  
- Evaluate all resumes against a selected job role  
- Rank candidates and display **Top N candidates**  
- Visualize missing skills across all resumes using a **heatmap**  
- Provides AI-driven suggestions for each candidate  

---

## Tech Stack

### Backend
- **Python** – Core language  
- **FastAPI** – API backend  
- **PyMuPDF / pdfplumber** – PDF text extraction  
- **python-docx / docx2txt** – DOCX parsing  
- **spaCy / NLTK** – Text cleaning & entity extraction  
- **LangChain / LangGraph / LangSmith** – LLM orchestration & debugging  
- **OpenAI GPT / GPT-4o-mini** – Semantic matching & AI feedback  
- **TF-IDF / BM25 / Fuzzy Matching** – Keyword matching  
- **Cosine Similarity / Weighted Score** – Final scoring  

### Frontend
- **Streamlit** – Interactive dashboard  
- **Pandas** – Data handling & visualization  

### Database
- **SQLite / PostgreSQL** – Optional storage for evaluation history  

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone <repository_url>
cd automated_resume_checker
python -m venv venv
venv\Scripts\activate   # Windows
pip install --upgrade pip
pip install -r requirements.txt

OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>

4. Run Backend
cd backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000

5. Run Frontend
cd frontend
streamlit run combined_dashboard_enhanced.py


=======
# Automated Resume Relevance Check System\n\nProject README content here.
# 📄 Automated Resume Relevance Check System

## Project Overview
The **Automated Resume Relevance Check System** is an AI-driven platform designed to streamline the resume evaluation process. It automatically compares resumes against job descriptions, generating a **relevance score (0–100)** for each candidate. The system highlights missing skills, certifications, or projects, and provides **AI-driven improvement suggestions**. It supports both **single and bulk resume evaluation**, ranks top candidates for each job role, and ensures fast, consistent, and data-driven shortlisting, reducing manual workload for placement teams.

---

## Features

### Single Resume Evaluation
- Upload one resume and one job description (PDF/DOCX)  
- Generate a **Relevance Score**  
- Identify missing skills, certifications, and projects  
- Receive **AI-generated improvement suggestions**  
- Verdict: **High / Medium / Low suitability**

### Bulk Resume Evaluation
- Upload multiple resumes and multiple job descriptions  
- Evaluate all resumes against a selected job role  
- Rank candidates and display **Top N candidates**  
- Visualize missing skills across all resumes using a **heatmap**  
- Provides AI-driven suggestions for each candidate  

---

## Tech Stack

### Backend
- **Python** – Core language  
- **FastAPI** – API backend  
- **PyMuPDF / pdfplumber** – PDF text extraction  
- **python-docx / docx2txt** – DOCX parsing  
- **spaCy / NLTK** – Text cleaning & entity extraction  
- **LangChain / LangGraph / LangSmith** – LLM orchestration & debugging  
- **OpenAI GPT / GPT-4o-mini** – Semantic matching & AI feedback  
- **TF-IDF / BM25 / Fuzzy Matching** – Keyword matching  
- **Cosine Similarity / Weighted Score** – Final scoring  

### Frontend
- **Streamlit** – Interactive dashboard  
- **Pandas** – Data handling & visualization  

### Database
- **SQLite / PostgreSQL** – Optional storage for evaluation history  

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone <repository_url>
cd automated_resume_checker
python -m venv venv
venv\Scripts\activate   # Windows
pip install --upgrade pip
pip install -r requirements.txt

OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>

4. Run Backend
cd backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000

5. Run Frontend
cd frontend
streamlit run combined_dashboard_enhanced.py


>>>>>>> 774f8cd (first commit)
Upload resumes and job descriptions to evaluate candidates.