import os
import threading
from src.logger import logging
from langchain_ollama import OllamaLLM
from src.utils import utils_functions


class JDParser:
    def __init__(
        self, llm_model="qwen3:latest", temperature=0.4, utility=utils_functions()
    ):
        self.llm_model = llm_model
        self.temperature = temperature
        self.llm_qwen = OllamaLLM(model=self.llm_model, temperature=self.temperature)
        self.utility_usage = utility

        logging.info("Warming up LLM...")
        _ = self.llm_qwen.invoke("Hello")  # Pre-load model
        logging.info("LLM is ready!")

        # Load JD prompt template
        prompt_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../prompt_templates/jd_prompt.txt")
        )
        if not os.path.exists(prompt_path):
            logging.error(f"JD prompt template not found at: {prompt_path}")
            raise FileNotFoundError(f"JD prompt template not found at: {prompt_path}")

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.jd_prompt_template = f.read()

    def parse(self, jd_text: str):
        """Parse a JD text into structured JSON using LLM."""
        try:
            jd_prompt = self.jd_prompt_template.format(jd_text=jd_text)
        except KeyError as e:
            logging.error(f"Error formatting JD prompt: {e}")
            return None

        done_flag = [False]
        spinner_thread = threading.Thread(
            target=self.utility_usage.spinner, args=(done_flag,), daemon=True
        )
        spinner_thread.start()
        logging.info("Sending request to LLM for JD parsing...")

        try:
            llm_output = self.llm_qwen.invoke(jd_prompt)
        except Exception as e:
            done_flag[0] = True
            spinner_thread.join()
            logging.error(f"Error during LLM invocation: {e}")
            return None

        done_flag[0] = True
        spinner_thread.join()

        jd_json = self.utility_usage.clean_text_into_json(llm_output)
        if jd_json:
            logging.info("JD parsing complete!")
        else:
            logging.warning("Failed to parse JD JSON output.")
        return jd_json
