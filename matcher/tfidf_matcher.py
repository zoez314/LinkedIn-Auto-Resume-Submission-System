import json

def load_jobs(path="data/jobs_cleaned.json"):
    """
    Load cleaned job data from JSON file.
    """
    with open(path, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    return jobs

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_match_scores(resume_text, jobs):
    """
    Compute TF-IDF similarity between resume and each job entry.
    """
    job_texts = [
        job["title"] + " " + job["company"] + " " + job["location"]
        for job in jobs
    ]

    texts = [resume_text] + job_texts  # resume is index 0
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compute cosine similarity between resume and each job
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    for i, score in enumerate(similarities):
        jobs[i]["match_score"] = round(float(score), 3)

    # Sort jobs by score descending
    sorted_jobs = sorted(jobs, key=lambda x: x["match_score"], reverse=True)

    return sorted_jobs
