from src.document_ingestion.pdf_processor import PDFProcessor
from src.parsers.cv_parsers import CVParser
from src.logger import logging


def process_cv_pdf():
    logging.info("Starting CV Processing")
    processor = PDFProcessor()
    docs = processor.process_pdf("data/MLE_CV_2025.pdf")
    cv_text = " ".join([doc.page_content for doc in docs])
    logging.info("Completed CV Processing")
    return cv_text


if __name__ == "__main__":
    cv_text = process_cv_pdf()
    print(cv_text)
    cv_parser = CVParser()
    cv_parse_json = cv_parser.parse(cv_text)
    print(cv_parse_json)
