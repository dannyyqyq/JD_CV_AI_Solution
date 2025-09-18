# JD_CV_AI_Solution

Using AI to extract, compare CV across JDs - An intelligent system for CV-Job Description matching and analysis.

## 🎯 Overview

This project allows users to:
- Upload a CV (PDF) and parse it into structured JSON
- Paste a Job Description (JD) and parse it into structured JSON
- Compare the CV against the JD and generate:
  - ATS alignment score
  - Matched and missing skills
  - Gap analysis and recommendations

The project uses Ollama LLM locally (qwen3-latest) for parsing and comparison, with a Streamlit web interface for easy user interaction.

## 🚀 Features

- **PDF CV Processing**: Automatically extract and parse CV content from PDF files
- **Job Description Analysis**: Parse job requirements, skills, and qualifications
- **AI-Powered Matching**: Compare CVs against job descriptions using local LLM
- **ATS Score Calculation**: Generate applicant tracking system alignment scores
- **Skills Gap Analysis**: Identify missing skills and provide improvement recommendations
- **Interactive Web Interface**: User-friendly Streamlit application
- **Local Processing**: All data processing happens locally using Ollama

## 📁 Folder Structure

```
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
│       ├── cv_vs_jd_prompt.txt
│       ├── cv_prompt.txt
│       └── jd_prompt.txt
│
├── main.py                  # Script used for testing
├── app.py                   # Main streamlit app POC
├── requirements_app.txt     # Minimal Python dependencies
├── requirements.txt         # Full dependencies including notebooks
└── README.md                # Project documentation
```

## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- [Ollama](https://ollama.ai/) installed and running
- qwen3-latest model downloaded via Ollama

### Step 1: Install Ollama

```bash
# On macOS
brew install ollama

# On Linux
curl -fsSL https://ollama.ai/install.sh | sh

# On Windows
# Download from https://ollama.ai/download
```

### Step 2: Pull the Required Model

```bash
ollama pull qwen3:latest
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/dannyyqyq/JD_CV_AI_Solution.git
cd JD_CV_AI_Solution
```

### Step 4: Install Python Dependencies

```bash
# For running the Streamlit app only
pip install -r requirements_app.txt

# For full development including notebooks
pip install -r requirements.txt
```

## 🚀 Usage

### Running the Streamlit Application

1. Start Ollama service:
```bash
ollama serve
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

### Using the Web Interface

1. **Upload CV**: Upload your PDF resume
2. **Paste Job Description**: Copy and paste the job description you're interested in
3. **Analyze**: Click to process and compare
4. **Review Results**: Get your ATS score, matched skills, and improvement recommendations

### Command Line Usage

For testing and development:

```bash
python main.py
```

## 📓 Development Notebooks

The `notebook/` directory contains Jupyter notebooks for experimentation and development:

1. **PDF_ingestion.ipynb**: Experiments with PDF processing and text extraction
2. **JD_CV_LLM_Parsing.ipynb**: Development of LLM prompts and parsing logic
3. **CV_JD_Engine.ipynb**: Core comparison and scoring algorithm development

## 🔧 Configuration

### Ollama Model Configuration

The system is configured to use `qwen3:latest`. To use a different model, update the model name in:
- `src/parsers/cv_parsers.py`
- `src/parsers/jd_parsers.py`
- `src/parsers/cv_vs_jd_parsers.py`

### Prompt Templates

Customize the AI behavior by editing prompt templates in `src/prompt_templates/`:
- `cv_prompt.txt`: Controls how CVs are parsed
- `jd_prompt.txt`: Controls how job descriptions are analyzed
- `cv_vs_jd_prompt.txt`: Controls the comparison and scoring logic

## 📊 Output Format

The system generates structured JSON outputs:

### CV Parsing Output
```json
{
  "personal_info": {...},
  "skills": [...],
  "experience": [...],
  "education": [...],
  "certifications": [...]
}
```

### Job Description Output
```json
{
  "requirements": [...],
  "skills_required": [...],
  "experience_level": "...",
  "qualifications": [...]
}
```

### Comparison Results
```json
{
  "ats_score": /10,
  "matched_skills": [...],
  "missing_skills": [...],
  "recommendations": [...],
  "gap_analysis": {...}
}
```
## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Ollama Connection Error**
- Ensure Ollama is running: `ollama serve`
- Open Ollama application running in backround
- Check if the model is installed: `ollama list`
  - If `qwen3:latest` is not within list, please do a `ollama pull qwen3:latest`
- Verify the model name matches in your configuration

**PDF Processing Issues**
- Ensure the PDF is text-based (not scanned images)

**Streamlit Not Starting**
- Verify all dependencies are installed
- Check Python version compatibility
- Ensure port 8501 is available

## 🔮 Future Enhancements

- [ ] Support for multiple CV formats (Word, HTML)
- [ ] Batch processing capabilities
- [ ] Advanced visualization dashboards
- [ ] Integration with job boards APIs
- [ ] Resume optimization suggestions
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] OpenAI APIS severless deployment

---

⭐ Feel free to play around!
