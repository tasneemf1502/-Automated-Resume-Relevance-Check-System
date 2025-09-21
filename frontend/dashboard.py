import streamlit as st
import requests

st.set_page_config(page_title="Resume Relevance Checker", layout="wide")
st.title("📄 Automated Resume Relevance Check System")

st.markdown("""
Upload a Resume and the corresponding Job Description (JD) to evaluate the candidate's relevance.
""")

with st.form("upload_form"):
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf","docx"])
    jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf","docx"])
    submit = st.form_submit_button("Evaluate Resume")

if submit:
    if resume_file and jd_file:
        files = {
            "resume": (resume_file.name, resume_file, "application/octet-stream"),
            "jd_file": (jd_file.name, jd_file, "application/octet-stream")
        }

        with st.spinner("Analyzing resume..."):
            try:
                response = requests.post("http://127.0.0.1:8000/evaluate_resume_with_jd/", files=files)
                response.raise_for_status()  # Raises error if status != 200
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
