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
```
Folder Structure

CV_Agent/
│
├── data/
│   ├── CV_2025.pdf
│   ├── jd_sample.txt
│   ├── cv_test.json
│   └── jd_test.json
│
├── notebook/
│   ├── 1. PDF_ingestion.ipynb
│   ├── 2. JD_CV_LLM_Parsing.ipynb
│   └── 3. CV_JD_Engine.ipynb
│
├── src/
│   ├── document_ingestion/
│   │   └── pdf_processor.py
│   ├── parsers/
│   │   ├── cv_parsers.py
│   │   ├── jd_parsers.py
│   │   └── cv_vs_jd_parsers.py
│   ├── utils_functions.py
│   ├── logger.py
│   └── prompt_templates/
│       ├── cd_vs_jd_prompt.txt
│       ├── cv_prompt.txt
│       └── jd_prompt.txt
├── main.py                           # Script used for testing
├── app.py                            # Main streamlit app POC
├── requirements_app.txt              # Minimal Python dependencies
├── requirements.txt                  # Full dependencies including using for notebooks experiments
└── README.md                         # Project documentation
