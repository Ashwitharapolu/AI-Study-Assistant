# ============================================
# pdf_loader.py - PDF Text Extraction Module
# AI Powered Smart Study Assistant
# ============================================

from pypdf import PdfReader


def extract_text(pdf_path):
    """
    Extract all text from a PDF file
    Args:
        pdf_path: Path to PDF file
    Returns:
        Extracted text as string or empty string on error
    """
    try:
        reader = PdfReader(pdf_path)

        # Check if PDF has pages
        if len(reader.pages) == 0:
            print("Error: PDF has no pages")
            return ""

        text = ""
        for page in reader.pages:
            try:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            except Exception as e:
                print(f"Warning: Could not extract page: {e}")
                continue

        # Check if any text was extracted
        if not text.strip():
            print("Error: No text could be extracted from PDF")
            return ""

        print(f"Successfully extracted {len(text)} characters")
        return text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""