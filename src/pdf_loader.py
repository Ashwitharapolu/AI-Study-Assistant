# Day 19 - PDF Loader with Error Handling
from pypdf import PdfReader

def extract_text(pdf_path):
    """Extract all text from a PDF file with error handling"""
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
                print(f"Warning: Could not extract text from page: {e}")
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

# Test it
if __name__ == "__main__":
    text = extract_text("data/sample.pdf")
    if text:
        print(f"Total characters: {len(text)}")
        print(f"First 200 characters: {text[:200]}")
    else:
        print("Failed to extract text!")