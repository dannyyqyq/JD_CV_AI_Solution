from langchain_ollama import OllamaLLM
import sys
import os
from src.utils import utils_functions

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))


class CVParser:
    def __init__(self, llm_model="qwen3:latest", temperature=0.5):
        self.llm_model = llm_model
        self.temperature = temperature

    def parse(self, cv_text):
        cv_prompt = f"""
You are a CV parsing assistant.

Extract the following fields from this CV text and return ONLY valid JSON inside a fenced code block (```json ... ```).
Do not output anything else.
Do not come out with your own information, all the information must only be extracted from the source itself.

Schema:
{{
  "summary": "As per below guidelines",
  "education": [
    {{
      "institution": "As per below guidelines",
      "degree": "As per below guidelines",
      "start_date": "mm/yyyy or yyyy",
      "end_date": "mm/yyyy or yyyy"
    }}
  ],
  "experience": [
    {{
      "job_title": "As per below guidelines",
      "company": "As per below guidelines (leave empty if freelance/self-employed)",
      "start_date": "mm/yyyy or yyyy or yyyy/mm",
      "end_date": "mm/yyyy or yyyy or yyyy/mm",
      "description": "As per below guidelines"
    }}
  ],
  "skills": ["As per below guidelines"],
  "projects": [
    {{
      "project_title": "As per below guidelines",
      "description": "As per below guidelines"
    }}
  ]
}}

Return fully populated JSON. Do not use ellipses `...`. If a section is missing, return [] or "".

Here is the CV text:

"{cv_text}"
"""
        # Invoke the LLM
        llm_qwen = OllamaLLM(model=self.llm_model, temperature=0.5)
        llm_output = llm_qwen.invoke(cv_prompt)

        # Clean and parse JSON
        utility_functions = utils_functions()
        cv_json = utility_functions.clean_text_into_json(llm_output)
        return cv_json
