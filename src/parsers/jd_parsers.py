import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))


class CVParser:
    def __init__(self, llm_model="qwen-ollama", temperature=0.5):
        self.llm_model = llm_model
        self.temperature = temperature
