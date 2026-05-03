import pdfplumber
import docx

def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    
    return ""