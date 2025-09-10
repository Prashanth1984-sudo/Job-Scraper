import pandas as pd
from scrapers.naukri_scraper import scrape_naukri_jobs
import os

def scrape_all(keyword, location, pages=1):
    print("Scraping Naukri...")
    jobs = scrape_naukri_jobs(keyword, location, pages)
    print(f"Naukri jobs fetched: {len(jobs)}")
    df = pd.DataFrame(jobs)
    return df

def save_jobs(df, filename="output/jobs.csv"):
    if not os.path.exists("output"):
        os.makedirs("output")
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} jobs to {filename}")
