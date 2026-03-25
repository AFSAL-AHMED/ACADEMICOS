"""
parser.py

Utility to extract text from syallbi or lecture notes.
Supports basic text files and PDFs.
"""

from PyPDF2 import PdfReader

def extract_text_from_file(file_path: str) -> str:
    """Extract text from a given file (txt or pdf)."""
    text = ""
    if file_path.endswith('.pdf'):
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading text file: {e}")
            return ""
    else:
        print("Unsupported file format. Please upload .pdf or .txt")
    
    return text.strip()
