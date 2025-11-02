from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from resume_parser import extract_skills_from_resume
from genai_skill_suggester import suggest_skills_with_genai
from job_matching import match_resume_with_jobs

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_resume():
    # --- Upload Resume File ---
    if 'resume' not in request.files:
        return redirect(url_for('index'))
    file = request.files['resume']
    if file.filename == '':
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # --- Extract Skills from Resume ---
    extracted_skills = extract_skills_from_resume(filepath)

    # --- Get Desired Job Titles from User ---
    desired_job_titles = [request.form.get('job_title')] if request.form.get('job_title') else []

    # --- Generate AI Skill Suggestions & Upskilling Advice ---
    ai_suggested_skills, upskilling_advice = suggest_skills_with_genai(extracted_skills, desired_job_titles)

    # --- Find Job Matches ---
    matched_jobs = match_resume_with_jobs(extracted_skills)

    # --- Calculate Resume Match Score ---
    if matched_jobs:
        best_match = max(matched_jobs, key=lambda x: x['match_percent'])
        match_score = best_match['match_percent']
    else:
        match_score = 0

    # --- Render the Results Page ---
    return render_template(
        'results.html',
        extracted_skills=extracted_skills,
        ai_suggested_skills=ai_suggested_skills,
        upskilling_advice=upskilling_advice,
        matched_jobs=matched_jobs,
        match_score=match_score
    )


if __name__ == '__main__':
    app.run(debug=True)
