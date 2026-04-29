def extract_text_from_pdf(uploaded_file) -> str:
    try:
        import fitz  # PyMuPDF
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages = [page.get_text() for page in doc]
        doc.close()
        return "\n".join(pages)
    except ImportError:
        return "[오류] PyMuPDF가 설치되지 않았습니다. 터미널에서 'pip install pymupdf' 를 실행하세요."
    except Exception as e:
        return f"[오류] PDF 텍스트 추출 실패: {e}"


def extract_first_page_image(pdf_bytes: bytes) -> str | None:
    """Returns base64-encoded PNG of the first page, or None on failure."""
    try:
        import fitz
        import base64
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0]
        mat = fitz.Matrix(1.5, 1.5)
        pix = page.get_pixmap(matrix=mat)
        png_bytes = pix.tobytes("png")
        doc.close()
        return base64.b64encode(png_bytes).decode()
    except Exception:
        return None
