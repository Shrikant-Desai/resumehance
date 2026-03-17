import io
import pdfplumber


def extract_pdf_text(file_input: bytes | str) -> str:
    """
    Extract plain text from a PDF.

    Args:
        file_input: Either raw PDF bytes (from an uploaded file) or a file path string.

    Returns:
        Extracted text as a single string.
    """
    full_text = ""

    # If bytes are passed (e.g. from FastAPI UploadFile), wrap in BytesIO
    source = io.BytesIO(file_input) if isinstance(file_input, bytes) else file_input

    with pdfplumber.open(source) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    return full_text
