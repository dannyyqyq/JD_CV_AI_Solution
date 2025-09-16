from src.document_ingestion.pdf_processor import PDFProcessor
from src.parsers.cv_parsers import CVParser
from src.parsers.jd_parsers import JDParser
from src.parsers.cv_vs_jd_parsers import CVvsJDParser
from src.logger import logging
import os
import json
import pprint


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


def load_jsons():
    cv_json_path = os.path.join("data", "cv_parsed_qwen.json")
    with open(cv_json_path, "r", encoding="utf-8") as f:
        cv_json = json.load(f)

    jd_json_path = os.path.join("data", "jd_parsed_qwen.json")
    with open(jd_json_path, "r", encoding="utf-8") as f:
        jd_json = json.load(f)

    return cv_json, jd_json


# if __name__ == "__main__":
# cv_text = process_cv_pdf()
# print(cv_text)
# cv_parser = CVParser()
# cv_parse_json = cv_parser.parse(cv_text)
# print(cv_parse_json)
# jd_file_path = os.path.join("data", "jd_sample.txt")
# jd_text = load_jd_text(jd_file_path)
# logging.info("Starting JD Parser...")
# jd_parser = JDParser()
# jd_parse_json = jd_parser.parse(jd_text)
# logging.info("JD Parser Compelted!")
# print(jd_parse_json)
# cv_json, jd_json = load_jsons()
# cv_vs_jd_parser = CVvsJDParser()
# comparison_json = cv_vs_jd_parser.compare_cv_vs_jd(cv_json, jd_json, industry="Technology")
# logging.info("CV vs JD Comparison Completed!")
# logging.info(pprint.pprint(comparison_json))


def main():
    logging.info("Starting CV vs JD parser test...")

    pdf_processor = PDFProcessor()
    cv_docs = pdf_processor.process_pdf("data/MLE_CV_2025.pdf")
    cv_text = " ".join([doc.page_content for doc in cv_docs])

    breakpoint()
    cv_parser = CVParser()
    cv_json = cv_parser.parse(cv_text)
    if not cv_json:
        logging.error("CV parsing failed!")
        return

    jd_file_path = os.path.join("data", "jd_sample.txt")
    with open(jd_file_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_parser = JDParser()
    jd_json = jd_parser.parse(jd_text)
    if not jd_json:
        logging.error("JD parsing failed!")
        return

    industry = "Technology"  # For now; later can come from UI dropdown
    cv_vs_jd_parser = CVvsJDParser()
    comparison_json = cv_vs_jd_parser.compare_cv_vs_jd(
        cv_json, jd_json, industry=industry
    )

    if comparison_json:
        logging.info("CV vs JD comparison complete!")
        # Pretty print results
        pprint.pprint(comparison_json)
    else:
        logging.error("CV vs JD comparison failed!")
