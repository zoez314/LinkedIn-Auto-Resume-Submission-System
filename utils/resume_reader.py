from pdfminer.high_level import extract_text as extract_pdf
from docx import Document

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file.
    """
    return extract_pdf(file)

def extract_text_from_docx(file):
    """
    Extract text from a Word (.docx) file.
    """
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])
