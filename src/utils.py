import re
import json
import time


class utils_functions:
    def clean_text_into_json(self, raw_input):
        """
        This function takes a raw string input and returns a valid JSON object extracted from it.
        """

        # 1. Remove <think> blocks if they exist

        cleaned_text = re.sub(r"<think>.*?</think>", "", raw_input, flags=re.DOTALL)

        # 2. Extract the JSON inside ```json ... ```
        match = re.search(r"```json\s*(\{.*?\})\s*```", cleaned_text, flags=re.DOTALL)
        if match:
            json_text = match.group(1)
        else:
            # fallback: extract from first { to last }
            start = cleaned_text.find("{")
            end = cleaned_text.rfind("}")
            json_text = cleaned_text[start : end + 1]

        # 3. Load JSON
        try:
            cv_json = json.loads(json_text)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
            print("Raw JSON text:")
            print(json_text)
            cv_json = None

        return cv_json

    def load_prompt(self, file_path, prompt_text):
        """
        This function loads a prompt from a file and replaces the placeholder {prompt_text} with the given prompt_text.

        Parameters:
            file_path (str): The path to the file containing the prompt.
            prompt_text (str): The text to replace the placeholder with.

        Returns:
            str: The loaded prompt with the placeholder replaced.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        return prompt.replace("{prompt_text}", prompt_text)

    def _spinner(self, done_flag):
        """Simple CLI spinner while LLM is running."""
        while not done_flag[0]:
            for cursor in "|/-\\":
                print(f"\rProcessing {cursor}", end="", flush=True)
                time.sleep(0.1)
        print("\r", end="")  # Clear line when done
