import json
from datetime import datetime
import os

DATA_FILE = "data/applied_jobs.json"

def load_applied_jobs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_job_record(job, status):
    job_record = {
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "date_applied": datetime.now().strftime("%Y-%m-%d"),
        "status": status  # "applied" or "saved"
    }
    jobs = load_applied_jobs()

    # Avoid duplicates
    if not any(j["title"] == job_record["title"] and j["company"] == job_record["company"] for j in jobs):
        jobs.append(job_record)
        with open(DATA_FILE, "w") as f:
            json.dump(jobs, f, indent=2)
        return True
    return False
