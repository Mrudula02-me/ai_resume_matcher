import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def suggest_skills_with_genai(extracted_skills, job_titles):
    """
    Uses OpenAI to suggest additional skills and provide upskilling recommendations
    based on the resume's extracted skills and desired job titles.
    """

    # Convert extracted skills and job titles into formatted text
    skills_text = ", ".join(extracted_skills) if extracted_skills else "None"
    jobs_text = ", ".join(job_titles) if job_titles else "None"

    prompt = f"""
You are an AI career mentor. Analyze the following resume skills and job roles, and do two things:
1. Suggest **additional technical and soft skills** the person should learn to better match the desired roles.
2. Provide **brief upskilling advice** — what tools, frameworks, or technologies they can explore next.

Resume Skills: {skills_text}
Desired Job Titles: {jobs_text}

Output format (in clean, structured points):
### AI Suggested Skills:
- Skill 1
- Skill 2
- Skill 3

### Upskilling Advice:
- Advice 1
- Advice 2
- Advice 3
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert career and technical mentor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        ai_text = response.choices[0].message.content.strip()

        # Split output into suggested skills and advice
        ai_suggested_skills = []
        upskilling_advice = []

        if "### AI Suggested Skills:" in ai_text:
            parts = ai_text.split("### AI Suggested Skills:")[1]
            if "### Upskilling Advice:" in parts:
                skills_part, advice_part = parts.split("### Upskilling Advice:")
            else:
                skills_part = parts
                advice_part = ""

            ai_suggested_skills = [
                line.replace("-", "").strip()
                for line in skills_part.split("\n")
                if line.strip().startswith("-")
            ]
            upskilling_advice = [
                line.replace("-", "").strip()
                for line in advice_part.split("\n")
                if line.strip().startswith("-")
            ]

        return ai_suggested_skills, upskilling_advice

    except Exception as e:
        print("Error while generating AI suggestions:", e)
        return [], []
