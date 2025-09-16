import os
import sys
import threading
from src.logger import logging
from langchain_ollama import OllamaLLM
from src.utils import utils_functions

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))

# class CVParser:
#     def __init__(self, llm_model="qwen3:latest", temperature=0.5):
#         self.llm_model = llm_model
#         self.temperature = temperature

#     def parse(self, cv_text):
#         cv_prompt = f"""
# You are a CV parsing assistant.

# Extract the following fields from this CV text and return ONLY valid JSON inside a fenced code block (```json ... ```).
# Do not output anything else.
# Do not come out with your own information, all the information must only be extracted from the source itself.

# Schema:
# {{
#   "summary": "As per below guidelines",
#   "education": [
#     {{
#       "institution": "As per below guidelines",
#       "degree": "As per below guidelines",
#       "start_date": "mm/yyyy or yyyy",
#       "end_date": "mm/yyyy or yyyy"
#     }}
#   ],
#   "experience": [
#     {{
#       "job_title": "As per below guidelines",
#       "company": "As per below guidelines (leave empty if freelance/self-employed)",
#       "start_date": "mm/yyyy or yyyy or yyyy/mm",
#       "end_date": "mm/yyyy or yyyy or yyyy/mm",
#       "description": "As per below guidelines"
#     }}
#   ],
#   "skills": ["As per below guidelines"],
#   "projects": [
#     {{
#       "project_title": "As per below guidelines",
#       "description": "As per below guidelines"
#     }}
#   ]
# }}

# Return fully populated JSON. Do not use ellipses `...`. If a section is missing, return [] or "".

# Here is the CV text:

# "{cv_text}"
# """
#         # Invoke the LLM
#         llm_qwen = OllamaLLM(model=self.llm_model, temperature=0.5)
#         llm_output = llm_qwen.invoke(cv_prompt)

#         # Clean and parse JSON
#         utility_functions = utils_functions()
#         cv_json = utility_functions.clean_text_into_json(llm_output)
#         return cv_json


class CVParser:
    def __init__(
        self, llm_model="qwen3:latest", temperature=0, utility=utils_functions()
    ):
        self.llm_model = llm_model
        self.temperature = temperature
        self.llm_qwen = OllamaLLM(model=self.llm_model, temperature=self.temperature)
        self.utility_usage = utility
        logging.info("Warming up LLM...")
        _ = self.llm_qwen.invoke("Hello")  # Pre-load model
        logging.info("LLM is ready!")

        # Load prompt template once
        prompt_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../prompt_templates/cv_prompt.txt")
        )
        if not os.path.exists(prompt_path):
            logging.error(f"Prompt template not found at: {prompt_path}")
            raise FileNotFoundError(f"Prompt template not found at: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.cv_prompt_template = f.read()

    def parse(self, cv_text: str):
        """Parse a CV text into structured JSON using LLM."""
        try:
            cv_prompt = self.cv_prompt_template.format(cv_text=cv_text)
        except KeyError as e:
            logging.error(f"Error formatting prompt: {e}")
            return None

        done_flag = [False]
        spinner_thread = threading.Thread(
            target=self.utility_usage._spinner, args=(done_flag,), daemon=True
        )
        spinner_thread.start()
        logging.info("Sending request to LLM...")

        try:
            llm_output = self.llm_qwen.invoke(cv_prompt)
        except Exception as e:
            done_flag[0] = True
            spinner_thread.join()
            logging.error(f"Error during LLM invocation: {e}")
            return None

        done_flag[0] = True
        spinner_thread.join()

        cv_json = self.utility_usage.clean_text_into_json(llm_output)
        if cv_json:
            logging.info("CV parsing complete!")
        else:
            logging.warning("Failed to parse CV JSON output.")
        return cv_json
