from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
import os

def scrape_linkedin_jobs(keyword, location, pages=2, delay=3, output_path="data/jobs.json"):
    """
    Scrape job listings from LinkedIn based on keyword and location.
    Saves results to a JSON file.
    """
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    jobs = []
    skipped = 0

    for page in range(pages):
        start = page * 25
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&start={start}"
        print(f"\n🔍 Scraping page {page+1}: {url}")
        driver.get(url)
        time.sleep(delay)

        listings = driver.find_elements(By.CLASS_NAME, "base-card")
        print(f"🔎 Found {len(listings)} job cards.")

        for card in listings:
            try:
                title = card.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
                company = card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
                location = card.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
                date_posted = card.find_element(By.TAG_NAME, "time").get_attribute("datetime")

                # ✅ Only include complete job listings
                if title and company and location:
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "date_posted": date_posted
                    })
                else:
                    skipped += 1
                    print("⚠️ Incomplete job card skipped.")

            except Exception as e:
                skipped += 1
                print("❌ Error parsing a job card:", e)

    driver.quit()

    # Save result
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(jobs)} valid jobs to {output_path}")
    print(f"🚫 Skipped {skipped} incomplete or failed job cards.")

# Optional test
if __name__ == "__main__":
    scrape_linkedin_jobs("data scientist", "California", pages=2)