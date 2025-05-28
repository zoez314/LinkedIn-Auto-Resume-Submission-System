# LinkedIn Auto-Resume Submission System — Feature Specification

## 🎯 Project Goal
Build an automated LinkedIn job application system that:
- Scrapes job postings from LinkedIn based on keyword and location.
- Parses uploaded resumes (PDF format).
- Matches resume content to job descriptions.
- Generates personalized cover letters using GPT.
- Prepares job applications for one-click submission or manual review.

## 🔧 Core Features (MVP)
1. **LinkedIn Job Scraper**
   - Simulate login, search jobs via keyword & location
   - Extract job title, company, location, description, and posting date

2. **Resume Parser**
   - Accept user-uploaded PDF resume
   - Extract raw text and key terms (skills, experience, education)

3. **Job-Resume Matcher**
   - Compute matching score between resume and job description
   - Use TF-IDF or Sentence-BERT for similarity

4. **Cover Letter Generator**
   - Use OpenAI GPT API to generate tailored cover letters
   - Input: job description + resume summary

5. **Application Manager**
   - Store applied/saved jobs in a local database
   - Enable one-click apply (if feasible) or manual export

6. **Frontend UI (Streamlit)**
   - Upload resume, input keywords/location
   - Display job list + match score + generate cover letter button

## ⚙️ Non-Functional Requirements
- Data stored in SQLite or JSON files
- Frontend built using Streamlit for rapid prototyping
- Modular codebase (scraper, parser, matcher, generator, UI)
- Sensitive info handled via `.env` (OpenAI API key, login creds)

## 🚫 Out-of-Scope for MVP
- Multi-resume or multi-template support
- Auto-click real "Apply" buttons on LinkedIn
- International language support

