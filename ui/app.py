# 0. Import dependencies
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from matcher.tfidf_matcher import load_jobs, compute_match_scores
from utils.resume_reader import extract_text_from_pdf, extract_text_from_docx
from gpt.letter_generator import generate_cover_letter

st.set_page_config(page_title="Resume Optimizer", layout="wide")
st.title("📄 Resume Optimizer for LinkedIn Jobs")

# 1. Upload Resume
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

# 2. Job Search Inputs
st.header("2. Job Search Parameters")
keyword = st.text_input("Job Title / Keyword", "data scientist")
location = st.text_input("Location", "California")

# 3. Matching Results
st.header("3. Matching Results")

if st.button("Find Matching Jobs"):
    if resume_text:
        jobs = load_jobs()
        st.session_state.matched_jobs = compute_match_scores(resume_text, jobs)
    else:
        st.warning("⚠️ Please paste your resume summary first.")

# ✅ Show Results
if "matched_jobs" in st.session_state and st.session_state.matched_jobs:
    st.subheader("Top Matching Jobs:")
    st.dataframe([
        {
            "Title": job.get("title", ""),
            "Company": job.get("company", ""),
            "Location": job.get("location", ""),
            "Score": round(job.get("match_score", 0), 3)
        }
        for job in st.session_state.matched_jobs[:10]
    ])


# 4. Cover Letter Generator
st.header("4. Generate Cover Letter")

user_name = st.text_input("Your Name", placeholder="e.g. Zoe")

if "generated_letter" not in st.session_state:
    st.session_state.generated_letter = ""

# ✅ Use matched_jobs from session_state
if "matched_jobs" in st.session_state and st.session_state.matched_jobs:
    job_options = [f"{job['title']} at {job['company']}" for job in st.session_state.matched_jobs]
    selected_job = st.selectbox("Select a job to apply for", job_options)
    selected_job_obj = st.session_state.matched_jobs[job_options.index(selected_job)]

    if st.button("✉️ Generate Cover Letter"):
        if not resume_text.strip():
            st.warning("Please upload or enter your resume first.")
        elif not user_name.strip():
            st.warning("Please enter your name.")
        else:
            st.session_state.generated_letter = generate_cover_letter(
                resume_summary=resume_text,
                job_description=selected_job_obj.get("description", "No description available."),
                job_title=selected_job_obj["title"],
                company_name=selected_job_obj["company"],
                user_name=user_name
            )

if st.session_state.generated_letter:
    st.subheader("Generated Cover Letter")
    st.text_area("You can edit below:", st.session_state.generated_letter, height=300)

# 5. Download Cover Letter
st.header("5. Download Cover Letter")

if st.session_state.generated_letter:
    # Convert to downloadable file
    st.download_button(
        label="💾 Download as .txt",
        data=st.session_state.generated_letter,
        file_name="cover_letter.txt",
        mime="text/plain"
    )

from utils.job_tracker import save_job_record, load_applied_jobs

# Save or Apply
st.header("5. Job Tracker")
if st.button("💾 Save this Job"):
    success = save_job_record(selected_job_obj, status="saved")
    if success:
        st.success("Job saved to your tracker.")
    else:
        st.info("This job is already in your saved list.")

if st.button("✅ Mark as Applied"):
    success = save_job_record(selected_job_obj, status="applied")
    if success:
        st.success("Job marked as applied.")
    else:
        st.info("This job is already marked.")

# Display current applied jobs
st.subheader("📋 Your Applied/Saved Jobs")
applied_jobs = load_applied_jobs()
st.table(applied_jobs[-5:])  # Show last 5 records


