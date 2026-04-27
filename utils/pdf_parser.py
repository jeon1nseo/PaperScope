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
