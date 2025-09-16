from src.document_ingestion.pdf_processor import PDFProcessor
from src.parsers.cv_parsers import CVParser
from src.parsers.jd_parsers import JDParser
from src.logger import logging
import os


def process_cv_pdf():
    logging.info("Starting CV Processing")
    processor = PDFProcessor()
    docs = processor.process_pdf("data/MLE_CV_2025.pdf")
    cv_text = " ".join([doc.page_content for doc in docs])
    logging.info("Completed CV Processing")
    return cv_text


def load_jd_text(file_path):
    """
    Load JD text from a .txt file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JD file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    return jd_text


if __name__ == "__main__":
    cv_text = process_cv_pdf()
    print(cv_text)
    cv_parser = CVParser()
    cv_parse_json = cv_parser.parse(cv_text)
    print(cv_parse_json)
    jd_file_path = os.path.join("data", "jd_sample.txt")
    jd_text = load_jd_text(jd_file_path)
    logging.info("Starting JD Parser...")
    jd_parser = JDParser()
    jd_parse_json = jd_parser.parse(jd_text)
    logging.info("JD Parser Compelted!")
    print(jd_parse_json)
