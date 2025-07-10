# 0. Import dependencies
import streamlit as st
import sys
import os
import json
import pandas as pd
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from matcher.tfidf_matcher import load_jobs, compute_match_scores
from utils.resume_reader import extract_text_from_pdf, extract_text_from_docx
from gpt.letter_generator import generate_cover_letter
from utils.job_tracker import save_job_record, load_applied_jobs

# Set up page
st.set_page_config(page_title="Resume Optimizer", layout="wide")
st.title("📄 Resume Optimizer for LinkedIn Jobs")

# 1. Upload Resume
st.markdown("---")
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
if not resume_text.strip():
    st.info("📄 Please upload your resume first.")

# 2. Job Search Inputs
st.markdown("---")
st.header("2. Job Search Parameters")
keyword = st.text_input("Job Title / Keyword", "data scientist")
location = st.text_input("Location", "California")

# 3. Matching Results
st.markdown("---")
st.header("3. Matching Results")

if st.button("🔍 Find Matching Jobs", key="find_jobs", use_container_width=True):
    if resume_text:
        with st.spinner("🔍 Matching jobs... please wait..."):
            jobs = load_jobs()
            st.session_state.matched_jobs = compute_match_scores(resume_text, jobs)
        if not st.session_state.matched_jobs:
            st.info("🧐 No jobs matched your resume. Try improving your resume or using a different keyword.")
        else:
            st.success("✅ Job matching complete!")
    else:
        st.warning("⚠️ Please upload or enter your resume first.")

if "matched_jobs" in st.session_state and st.session_state.matched_jobs:
    st.subheader("🎯 Top Matching Jobs")
    top_jobs = st.session_state.matched_jobs[:10]

    df_top = pd.DataFrame([
        {
            "Job Title": ("🔥 Top Match: " if i < 3 else "") + job.get("title", ""),
            "Company": job.get("company", ""),
            "Location": job.get("location", ""),
            "Match Score (%)": f"{round(job.get('match_score', 0) * 100, 1)}%"
        } for i, job in enumerate(top_jobs)
    ])
    st.dataframe(df_top, use_container_width=True)
else:
    st.info("🔎 No matching jobs yet. Please upload resume and click 'Find Matching Jobs'.")

# 4. Cover Letter Generator
st.markdown("---")
st.header("4. Generate Cover Letter")

user_name = st.text_input("Your Name", placeholder="e.g. Zoe")

if "generated_letter" not in st.session_state:
    st.session_state.generated_letter = ""

if "matched_jobs" in st.session_state and st.session_state.matched_jobs:
    job_options = [f"{job['title']} at {job['company']}" for job in st.session_state.matched_jobs]
    selected_job = st.selectbox("Select a job to apply for", job_options)
    selected_job_obj = st.session_state.matched_jobs[job_options.index(selected_job)]

    if st.button("✉️ Generate Cover Letter", key="generate_cover_letter", use_container_width=True):
        if not resume_text.strip():
            st.warning("⚠️ Please upload or enter your resume first.")
        elif not user_name.strip():
            st.warning("⚠️ Please enter your name.")
        else:
            with st.spinner("✍️ Generating your personalized cover letter..."):
                st.session_state.generated_letter = generate_cover_letter(
                    resume_summary=resume_text,
                    job_description=selected_job_obj.get("description", "No description available."),
                    job_title=selected_job_obj["title"],
                    company_name=selected_job_obj["company"],
                    user_name=user_name
                )
            st.success("✅ Cover letter generated!")
else:
    st.info("📄 Please match jobs before generating a cover letter.")

if st.session_state.generated_letter:
    st.subheader("📄 Generated Cover Letter")
    st.text_area("You can edit below:", st.session_state.generated_letter, height=400)

# 5. Download Cover Letter
st.markdown("---")
st.header("5. Download Cover Letter")
if st.session_state.generated_letter:
    st.download_button(
        label="⬇️ Download Cover Letter as .txt",
        data=st.session_state.generated_letter,
        file_name="cover_letter.txt",
        mime="text/plain",
        use_container_width=True
    )

# 6. Job Tracker
st.markdown("---")
st.header("6. Job Tracker")
if "matched_jobs" in st.session_state and st.session_state.matched_jobs:
    if st.button("📅 Save this Job", key="save_job", use_container_width=True):
        success = save_job_record(selected_job_obj, status="saved")
        if success:
            st.success("Job saved to your tracker.")
        else:
            st.info("This job is already in your saved list.")

    if st.button("✅ Mark as Applied", key="mark_applied", use_container_width=True):
        success = save_job_record(selected_job_obj, status="applied")
        if success:
            st.success("Job marked as applied.")
        else:
            st.info("This job is already marked.")

    st.subheader("📋 Your Applied/Saved Jobs")
    applied_jobs = load_applied_jobs()
    if applied_jobs:
        st.table(applied_jobs[-5:])
    else:
        st.info("You haven’t saved or applied to any jobs yet.")

# 7. Application History
st.markdown("---")
st.header("📂 Application History")

applied_jobs_path = "data/applied_jobs.json"
if os.path.exists(applied_jobs_path):
    with open(applied_jobs_path, "r") as f:
        records = json.load(f)

    if records:
        st.subheader("📝 Your Jobs")

        for record in records:
            if "uid" not in record:
                record["uid"] = str(uuid.uuid4())

        with open(applied_jobs_path, "w") as f:
            json.dump(records, f, indent=2)

        for record in records[-5:][::-1]:
            with st.container():
                st.markdown(f"""
                **🧒 {record.get('title', 'No Title')}** at **{record.get('company', 'Unknown')}**  
                📍 {record.get('location', '')} | 🗕️ {record.get('date_posted', '')}  
                🏷️ Status: `{record.get('status', 'unknown')}`
                """)
                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button("🗑 Delete", key=f"delete_{record['uid']}"):
                        records = [r for r in records if r["uid"] != record["uid"]]
                        with open(applied_jobs_path, "w") as f:
                            json.dump(records, f, indent=2)
                        st.experimental_rerun()

        df_hist = pd.DataFrame(records)
        csv_data = df_hist.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Job History as CSV",
            data=csv_data,
            file_name='job_application_history.csv',
            mime='text/csv',
            use_container_width=True
        )
    else:
        st.info("📭 You haven’t saved or applied to any jobs yet. Start exploring now!")
