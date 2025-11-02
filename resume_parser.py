import re
import docx2txt
import PyPDF2
import os

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    return docx2txt.process(file_path)


def extract_skills_from_resume(file_path):
    """
    Extracts technical and soft skills from a resume file (PDF or DOCX)
    using basic keyword matching.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

    # Example skill keywords
    skill_keywords = [
        "python", "java", "flask", "django", "machine learning", "deep learning",
        "opencv", "html", "css", "javascript", "sql", "power bi", "pandas", "numpy",
        "ai", "data analysis", "communication", "leadership", "teamwork"
    ]

    # Extract skills present in resume text
    extracted_skills = []
    for skill in skill_keywords:
        if re.search(rf"\b{skill}\b", text, re.IGNORECASE):
            extracted_skills.append(skill.title())

    return extracted_skills
