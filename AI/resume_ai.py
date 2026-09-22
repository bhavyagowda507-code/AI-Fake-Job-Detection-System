import pdfplumber
import docx

def extract_resume_text(file_path):

    text = ""

    if file_path.endswith(".pdf"):

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

    elif file_path.endswith(".docx"):

        doc = docx.Document(file_path)

        for para in doc.paragraphs:
            text += para.text

    return text