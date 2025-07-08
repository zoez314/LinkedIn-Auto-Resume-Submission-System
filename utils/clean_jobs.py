import json
import os

def clean_jobs(input_path="data/jobs.json", output_path="data/jobs_cleaned.json"):
    # Load raw job data
    with open(input_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    print(f"🔍 Loaded {len(jobs)} job records.")

    # Filter out jobs with missing fields
    cleaned = [
        job for job in jobs
        if job.get("title") and job.get("company") and job.get("location")
    ]

    # Save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(cleaned)} cleaned jobs to {output_path}")

if __name__ == "__main__":
    clean_jobs()