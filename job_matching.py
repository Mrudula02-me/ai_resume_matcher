# job_matching.py
def match_resume_with_jobs(extracted_skills):
    """
    Matches resume skills with predefined job roles and returns the best fits.
    """

    # Example job database (you can replace this with real API data later)
    job_database = [
        {
            "title": "Data Analyst",
            "skills": ["Python", "SQL", "Excel", "Power BI", "Data Visualization"]
        },
        {
            "title": "Machine Learning Engineer",
            "skills": ["Python", "TensorFlow", "Scikit-learn", "Pandas", "Numpy"]
        },
        {
            "title": "AI Engineer",
            "skills": ["Deep Learning", "Computer Vision", "OpenCV", "PyTorch", "NLP"]
        },
        {
            "title": "Web Developer",
            "skills": ["HTML", "CSS", "JavaScript", "Flask", "React"]
        }
    ]

    matched_jobs = []

    for job in job_database:
        match_count = len(set(extracted_skills).intersection(set(job["skills"])))
        if match_count > 0:
            match_percent = (match_count / len(job["skills"])) * 100
            matched_jobs.append({
                "title": job["title"],
                "skills": job["skills"],
                "match_percent": round(match_percent, 2)
            })

    # Sort jobs by match percentage
    matched_jobs = sorted(matched_jobs, key=lambda x: x["match_percent"], reverse=True)

    return matched_jobs

