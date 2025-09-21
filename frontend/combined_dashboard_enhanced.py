import streamlit as st
import requests
import pandas as pd
from io import BytesIO
import time
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

st.set_page_config(page_title="Resume Relevance Checker", layout="wide")
st.title("📄 Automated Resume Relevance Check System - Enhanced Dashboard")

tabs = st.tabs(["Single Resume Evaluation", "Bulk Resume Evaluation"])

def color_verdict(verdict):
    return "green" if verdict=="High" else ("orange" if verdict=="Medium" else "red")

def evaluate_resume(resume_file, jd_file):
    resume_file.seek(0)
    jd_file.seek(0)
    files = {
        "resume": (resume_file.name, resume_file, "application/octet-stream"),
        "jd_file": (jd_file.name, jd_file, "application/octet-stream")
    }
    try:
        response = requests.post("http://127.0.0.1:8000/evaluate_resume_with_jd/", files=files)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error connecting to backend: {e}"}
    return response.json()

# ---------------------------
# Tab 1: Single Resume
# ---------------------------
with tabs[0]:
    st.subheader("Evaluate One Resume Against One Job Description")
    with st.form("single_upload_form"):
        resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf","docx"])
        jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf","docx"])
        submit_single = st.form_submit_button("Evaluate Resume")

    if submit_single and resume_file and jd_file:
        with st.spinner("Analyzing resume..."):
            result = evaluate_resume(resume_file, jd_file)
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("✅ Evaluation Complete!")
            st.write(f"**Resume:** {result['resume_file']}")
            st.write(f"**JD:** {result['jd_file']}")
            st.write(f"**Score:** {result['score']} / 100")
            st.markdown(f"**Verdict:** <span style='color:{color_verdict(result['verdict'])}; font-weight:bold'>{result['verdict']}</span>", unsafe_allow_html=True)
            st.write(f"**Missing Skills:** {', '.join(result['missing_skills']) if result['missing_skills'] else 'None'}")
            st.write("**AI Suggestions:**")
            st.info(result['ai_feedback'])

# ---------------------------
# Tab 2: Bulk Resume
# ---------------------------
with tabs[1]:
    st.subheader("Evaluate Multiple Resumes Against Multiple Job Descriptions")
    with st.form("bulk_upload_form"):
        resumes = st.file_uploader("Upload Resumes (PDF/DOCX) - multiple allowed", type=["pdf","docx"], accept_multiple_files=True)
        jds = st.file_uploader("Upload Job Descriptions (PDF/DOCX) - multiple allowed", type=["pdf","docx"], accept_multiple_files=True)
        submit_bulk = st.form_submit_button("Evaluate Resumes")

    if submit_bulk:
        if resumes and jds:
            role_dict = {jd.name: jd for jd in jds}
            selected_role = st.selectbox("Select Job Role to Evaluate Resumes Against:", list(role_dict.keys()))
            selected_jd_file = role_dict[selected_role]

            all_results = []
            progress_bar = st.progress(0)

            for i, resume_file in enumerate(resumes):
                with st.spinner(f"Evaluating {resume_file.name}..."):
                    result = evaluate_resume(resume_file, selected_jd_file)
                if "error" in result:
                    st.error(f"{resume_file.name}: {result['error']}")
                    continue
                all_results.append({
                    "Resume": result['resume_file'],
                    "Score": result['score'],
                    "Verdict": result['verdict'],
                    "Missing Skills": ", ".join(result['missing_skills']) if result['missing_skills'] else "None",
                    "AI Suggestions": result['ai_feedback']
                })
                progress_bar.progress((i+1)/len(resumes))
                time.sleep(2)

            if all_results:
                df = pd.DataFrame(all_results)
                st.subheader(f"📊 Evaluation Results for {selected_role}")
                st.dataframe(df)

                # Top Candidates
                st.subheader(f"🏆 Top Candidates for {selected_role}")
                top_n = st.slider("Select Top N Candidates", 1, min(10, len(df)), 3)
                top_candidates = df.nlargest(top_n, 'Score')
                st.dataframe(top_candidates)
