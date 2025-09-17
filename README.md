# CV vs JD Comparison Agent

## Description

This project allows users to:

- Upload a CV (PDF) and parse it into structured JSON.
- Paste a Job Description (JD) and parse it into structured JSON.
- Compare the CV against the JD and generate:
  - ATS alignment score
  - Matched and missing skills
  - Gap analysis and recommendations

The project uses **Ollama LLM locally** for parsing and comparison, and a **Streamlit web interface** for easy user interaction.

---

## Folder Structure

CV_Agent/
│
├── data/
│   ├── MLE_CV_2025.pdf          # Sample CV for testing
│   ├── jd_sample.txt            # Sample JD for testing
│   ├── cv_test.json             # Saved CV JSON for testing
│   └── jd_test.json             # Saved JD JSON for testing
│
├── prompt_templates/
│   ├── cv_prompt.txt            # CV parsing prompt template
│   └── jd_prompt.txt            # JD parsing prompt template
│
├── src/
│   ├── app.py                   # Streamlit app
│   ├── logger.py                # Logging setup
│   ├── llm.py                   # LLM wrapper (Ollama / OpenAI)
│   ├── utils/
│   │   └── utils_functions.py   # Utility functions (JSON parsing, spinner, etc.)
│   ├── document_ingestion/
│   │   └── pdf_processor.py     # PDF extraction
│   └── parsers/
│       ├── cv_parsers.py        # CV parser
│       ├── jd_parsers.py        # JD parser
│       └── cv_vs_jd_parsers.py  # Comparison parser
│
├── requirements_app.txt         # Minimal Python dependencies
└── README.md                    # Project documentation
