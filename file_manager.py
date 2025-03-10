import os
from PyPDF2 import PdfReader
from docx import Document

class FileManager:
    @staticmethod
    def save_uploaded_file(uploaded_file, folder="uploads"):
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path

    @staticmethod
    def extract_text_from_file(file_path):
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                return "".join([page.extract_text() for page in reader.pages])
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            with open(file_path, 'r') as file:
                return file.read()
