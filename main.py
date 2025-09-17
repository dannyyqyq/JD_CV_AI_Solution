from src.document_ingestion.pdf_processor import PDFProcessor
from src.parsers.cv_parsers import CVParser
from src.parsers.jd_parsers import JDParser
from src.parsers.cv_vs_jd_parsers import CVvsJDParser
from src.logger import logging
import os
import pprint


def cv_jd_comparison(industry="Technology"):  # For now; later can come from UI dropdown
    logging.info("Starting CV vs JD parser test...")
    try:
        pdf_processor = PDFProcessor()
        cv_docs = pdf_processor.process_pdf("data/MLE_CV_2025.pdf")
        cv_text = " ".join([doc.page_content for doc in cv_docs])

        cv_parser = CVParser()
        cv_json = cv_parser.parse(cv_text)

        jd_file_path = os.path.join("data", "jd_sample.txt")
        with open(jd_file_path, "r", encoding="utf-8") as f:
            jd_text = f.read()

        jd_parser = JDParser()
        jd_json = jd_parser.parse(jd_text)

        cv_vs_jd_parser = CVvsJDParser()
        comparison_json = cv_vs_jd_parser.compare_cv_vs_jd(
            cv_json,
            jd_json,
            industry=industry,  # For now; later can come from UI dropdown
        )

        if comparison_json:
            pprint.pprint(comparison_json)  # Pretty print results
        else:
            logging.error("CV vs JD comparison failed!")
    except Exception as e:
        logging.error(f"Main function failed: {e}")


if __name__ == "__main__":
    cv_jd_comparison()
