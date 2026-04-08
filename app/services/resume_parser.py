from io import BytesIO

from docx import Document
from pypdf import PdfReader


class UnsupportedResumeTypeError(ValueError):
    pass


class ResumeParser:
    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}

    def parse_bytes(self, filename: str, content: bytes) -> str:
        extension = self._extension(filename)
        if extension not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedResumeTypeError(
                f"Unsupported extension '{extension}'. Supported: {sorted(self.SUPPORTED_EXTENSIONS)}"
            )

        if extension == ".pdf":
            return self._parse_pdf(content)
        if extension == ".docx":
            return self._parse_docx(content)
        return content.decode("utf-8", errors="ignore")

    @staticmethod
    def _extension(filename: str) -> str:
        if "." not in filename:
            return ""
        return f".{filename.rsplit('.', 1)[-1].lower()}"

    @staticmethod
    def _parse_pdf(content: bytes) -> str:
        reader = PdfReader(BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text.strip()

    @staticmethod
    def _parse_docx(content: bytes) -> str:
        doc = Document(BytesIO(content))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs).strip()
