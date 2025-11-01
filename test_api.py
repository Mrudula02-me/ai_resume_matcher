from job_api import fetch_jobs

jobs = fetch_jobs("Data Scientist")

print(f"Total jobs fetched: {len(jobs)}")

if jobs:
    print("Sample job:")
    print(jobs[0])
