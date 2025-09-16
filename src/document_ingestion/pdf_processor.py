from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader


class PDFProcessor:
    """Advance PDF parsing"""

    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )

    def process_pdf(self, pdf_path: str) -> List[Document]:
        """Process a PDF and return a list of chunked documents."""

        # Load the PDF
        loader = PyPDFLoader(pdf_path)

        # Load the document and split it into chunks in one step
        documents = loader.load_and_split(text_splitter=self.text_splitter)

        return documents
