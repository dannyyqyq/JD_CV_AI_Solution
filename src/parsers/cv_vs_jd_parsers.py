import threading
import logging
from langchain_ollama import OllamaLLM
from src.utils import utils_functions
import os


class CVvsJDParser:
    def __init__(
        self, llm_model="qwen3:latest", temperature=0.5, utility=utils_functions()
    ):
        self.llm_model = llm_model
        self.temperature = temperature
        self.llm = OllamaLLM(model=self.llm_model, temperature=self.temperature)
        self.utility_usage = utility

        # Load prompt template
        prompt_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "../prompt_templates/cd_vs_jd_prompt.txt"
            )
        )
        if not os.path.exists(prompt_path):
            logging.error(f"Prompt template not found at: {prompt_path}")
            raise FileNotFoundError(
                f"CD vs JD prompt template not found at: {prompt_path}"
            )

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.cv_vs_jd_prompt_template = f.read()

    def compare_cv_vs_jd(self, cv_json, jd_json, industry="Technology"):
        try:
            prompt = self.cv_vs_jd_prompt_template.format(
                cv_json=cv_json, jd_json=jd_json, industry=industry
            )
        except KeyError as e:
            logging.error(f"Error formatting CV-vs-JD prompt: {e}")
            return None

        logging.info("Sending request to LLM for CV vs JD comparison...")

        done_flag = [False]
        spinner_thread = threading.Thread(
            target=self.utility_usage.spinner, args=(done_flag,)
        )
        spinner_thread.start()

        try:
            llm_output = self.llm.invoke(prompt)
        except Exception as e:
            done_flag[0] = True
            spinner_thread.join()
            logging.error(f"Error during LLM invocation: {e}")
            return None

        done_flag[0] = True
        spinner_thread.join()

        comparison_json = self.utility_usage.clean_text_into_json(llm_output)
        logging.info("CV vs JD comparison complete")
        return comparison_json
