def extract_skills(text):
    skills_db = ["python", "machine learning", "nlp", "sql", "excel",
                 "deep learning", "tensorflow", "pytorch", "react", "javascript"]

    text = text.lower()
    found = [skill for skill in skills_db if skill in text]

    return list(set(found))