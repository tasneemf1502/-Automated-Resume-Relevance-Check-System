# backend/app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import docx2txt
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import openai

# ----------------------------
# Load environment variables for OpenAI API
# ----------------------------
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------
# Initialize NLP model
# ----------------------------
nlp = spacy.load("en_core_web_sm")

# ----------------------------
# FastAPI app setup
# ----------------------------
app = FastAPI(title="Automated Resume Relevance Check System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Helper functions
# ----------------------------
def extract_text(file: UploadFile):
    file.file.seek(0)  # reset pointer
    content = file.file.read()
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif file.filename.endswith(".docx"):
        file.file.seek(0)
        return docx2txt.process(file.file)
    return content.decode("utf-8")

def clean_text(text: str):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def keyword_hard_match(resume_text: str, jd_text: str):
    resume_words = set(resume_text.split())
    jd_words = set(jd_text.split())
    matched = resume_words & jd_words
    missing = jd_words - resume_words
    return matched, missing

def semantic_score(resume_text: str, jd_text: str):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return score * 100  # scale 0-100

def ai_feedback(resume_text: str, jd_text: str):
    prompt = f"""
    Evaluate this resume against the following job description:
    Job Description: {jd_text}
    Resume: {resume_text}

    Give a short evaluation with missing skills, gaps, and suggestions.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            max_tokens=300
        )
        feedback = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        feedback = f"AI feedback unavailable: {e}"
    return feedback

# ----------------------------
# Evaluation Endpoint
# ----------------------------
@app.post("/evaluate_resume_with_jd/")
async def evaluate_resume_with_jd(resume: UploadFile = File(...), jd_file: UploadFile = File(...)):
    try:
        resume_text = clean_text(extract_text(resume))
        jd_text = clean_text(extract_text(jd_file))

        matched_keywords, missing_keywords = keyword_hard_match(resume_text, jd_text)
        semantic_similarity = semantic_score(resume_text, jd_text)

        hard_match_score = (len(matched_keywords) / (len(matched_keywords)+len(missing_keywords)+1e-5)) * 100
        final_score = 0.5*hard_match_score + 0.5*semantic_similarity

        verdict = "High" if final_score>=75 else ("Medium" if final_score>=50 else "Low")
        feedback = ai_feedback(resume_text, jd_text)

        return {
            "resume_file": resume.filename,
            "jd_file": jd_file.filename,
            "score": round(final_score, 2),
            "verdict": verdict,
            "missing_skills": list(missing_keywords),
            "ai_feedback": feedback
        }
    except Exception as e:
        return {"error": str(e)}
