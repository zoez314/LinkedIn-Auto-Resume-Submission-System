import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from matcher.tfidf_matcher import load_jobs, compute_match_scores

# App title
st.set_page_config(page_title="Resume Optimizer", layout="wide")
st.title("📄 Resume Optimizer for LinkedIn Jobs")

#Upload resume section
from utils.resume_reader import extract_text_from_pdf, extract_text_from_docx

st.header("1. Upload Your Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

resume_text = ""
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            st.warning("Unsupported file type.")
        st.success("✅ Resume uploaded and parsed successfully!")
    except Exception as e:
        st.error(f"❌ Failed to extract text: {e}")

resume_text = st.text_area("Resume Summary (editable)", resume_text, height=200)


# Search inputs
st.header("2. Job Search Parameters")
keyword = st.text_input("Job Title / Keyword", "data scientist")
location = st.text_input("Location", "California")

# Trigger matching
st.header("3. Matching Results")
if st.button("Find Matching Jobs"):
    if resume_text:
        jobs = load_jobs()
        matched = compute_match_scores(resume_text, jobs)

        # Format results
        st.subheader("Top Matching Jobs:")
        st.dataframe(
            [{ 
                "Title": job["title"],
                "Company": job["company"],
                "Location": job["location"],
                "Score": job["match_score"]
            } for job in matched[:10]]
        )
    else:
        st.warning("⚠️ Please paste your resume summary first.")
