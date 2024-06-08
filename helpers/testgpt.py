import json
from pathlib import Path
import requests

class TestGPT:
    def __init__(self, config_file="testgpt_prompting.json"):
        self.api_key = self.get_api_key()
        self.config_file = config_file
        self.initial_parameters = self.get_initial_parameters()
        self.get_api_key()


    def get_api_key(self): 
       self_path = Path(globals().get("__file__", "./_")).absolute().parent
       print(self_path)
       env_path = "../env.json"
       config_file = self_path / env_path
       with open(config_file) as f:
             return json.load(f)["api_key_for_chatgbt"]
         
    def get_initial_parameters(self):
        self_path = Path(globals().get("__file__", "./_")).absolute().parent
        config_file = self_path / self.config_file
        with open(config_file) as f:
            return json.load(f)

    def _generate_data(self, note, data_type):
        if data_type not in self.initial_parameters["prompts"]:
            raise ValueError(
                f"Data type {data_type} not found in config file {self.config_file}"
            )
        if not note:
            raise ValueError("The given data was empty, we can't generate any data")
        
        endpoint = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        parameters = {
            "model": self.initial_parameters["model"],
            "messages": self.initial_parameters["prompts"][data_type]["messages"],
        }
        parameters["messages"].append({"role": "user", "content": note})
        print(parameters)
        try:
            response = requests.post(endpoint, headers=headers, json=parameters)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            print(e.response.text)
            result = None
        except Exception as e:
            print(e)
            result = None
        
        return result

    def generate_open_question(self, note):
        return self._generate_data(note, "open_question")

    def generate_multiple_choice_question(self, note):
        return self._generate_data(note, "multiple_choice_question")
    
    def generate_answer(self,question): 
        return self._generate_data(question, "answer")


if __name__ == "__main__":
    api_key = "TestGpt"
    test_gpt = TestGPT(api_key)
    test_text = """
    De grutto is een oer-Hollandse weidevogel. Je vindt deze grote, slanke steltloper op erven en graslanden van
    boerenbedrijven waar voldoende ruimte is voor natuur. Het meest ideaal zijn vochtige, kruidenrijke graslanden met een
    goed bodemleven en volop insecten aan de oppervlakte.
    """
    result = test_gpt.generate_open_question(test_text)
    print(result)
    result = test_gpt.generate_multiple_choice_question(test_text)
    print(result)
