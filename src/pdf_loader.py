# Day 3 - PDF Text Extraction
from pypdf import PdfReader

def extract_text(pdf_path):
    """Extract all text from a PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Test it
if __name__ == "__main__":
    pdf_path = "data/sample.pdf"
    text = extract_text(pdf_path)
    print(f"Total characters extracted: {len(text)}")
    print("\nFirst 500 characters:")
    print(text[:500])