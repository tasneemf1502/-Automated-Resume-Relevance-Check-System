import streamlit as st
import requests
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Resume Relevance Checker", layout="wide")
st.title("📄 Automated Resume Relevance Check System")

tabs = st.tabs(["Single Resume Evaluation", "Bulk Resume Evaluation"])

# ---------------------------
# Tab 1: Single Resume Evaluation
# ---------------------------
with tabs[0]:
    st.subheader("Evaluate One Resume Against One Job Description")
    with st.form("single_upload_form"):
        resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf","docx"])
        jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf","docx"])
        submit_single = st.form_submit_button("Evaluate Resume")

    if submit_single:
        if resume_file and jd_file:
            files = {
                "resume": (resume_file.name, resume_file, "application/octet-stream"),
                "jd_file": (jd_file.name, jd_file, "application/octet-stream")
            }

            with st.spinner("Analyzing resume..."):
                try:
                    response = requests.post("http://127.0.0.1:8000/evaluate_resume_with_jd/", files=files)
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to backend: {e}")
                else:
                    result = response.json()
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success("✅ Evaluation Complete!")
                        st.write(f"**Resume File:** {result['resume_file']}")
                        st.write(f"**JD File:** {result['jd_file']}")
                        st.write(f"**Score:** {result['score']} / 100")
                        st.write(f"**Verdict:** {result['verdict']}")
                        st.write(f"**Missing Skills / Keywords:** {', '.join(result['missing_skills']) if result['missing_skills'] else 'None'}")
                        st.write("**AI Suggestions:**")
                        st.info(result['ai_feedback'])
        else:
            st.warning("Please upload both Resume and Job Description.")

# ---------------------------
# Tab 2: Bulk Resume Evaluation
# ---------------------------
with tabs[1]:
    st.subheader("Evaluate Multiple Resumes Against Multiple Job Descriptions")
    with st.form("bulk_upload_form"):
        resumes = st.file_uploader(
            "Upload Resumes (PDF/DOCX) - You can select multiple files", 
            type=["pdf","docx"], 
            accept_multiple_files=True
        )
        jds = st.file_uploader(
            "Upload Job Descriptions (PDF/DOCX) - You can select multiple files", 
            type=["pdf","docx"], 
            accept_multiple_files=True
        )
        submit_bulk = st.form_submit_button("Evaluate All Resumes")

    if submit_bulk:
        if resumes and jds:
            final_results = []

            for resume_file in resumes:
                for jd_file in jds:
                    files = {
                        "resume": (resume_file.name, resume_file, "application/octet-stream"),
                        "jd_file": (jd_file.name, jd_file, "application/octet-stream")
                    }

                    with st.spinner(f"Evaluating {resume_file.name} against {jd_file.name}..."):
                        try:
                            response = requests.post("http://127.0.0.1:8000/evaluate_resume_with_jd/", files=files)
                            response.raise_for_status()
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to backend for {resume_file.name} and {jd_file.name}: {e}")
                            continue
                        else:
                            result = response.json()
                            if "error" in result:
                                st.error(f"{resume_file.name} vs {jd_file.name}: {result['error']}")
                                continue
                            # Append results
                            final_results.append({
                                "Resume": result['resume_file'],
                                "JD": result['jd_file'],
                                "Score": result['score'],
                                "Verdict": result['verdict'],
                                "Missing Skills": ", ".join(result['missing_skills']) if result['missing_skills'] else "None",
                                "AI Suggestions": result['ai_feedback']
                            })

            if final_results:
                st.success("✅ Bulk Evaluation Complete!")
                df = pd.DataFrame(final_results)
                st.dataframe(df)

                # Download CSV
                csv_buffer = BytesIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_buffer.getvalue(),
                    file_name="bulk_resume_evaluation.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Please upload both resumes and job descriptions.")
