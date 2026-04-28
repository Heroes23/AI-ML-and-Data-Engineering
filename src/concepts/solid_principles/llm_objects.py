# Class
class ChatGPT:
    # Constructor
    def __init__(self, api_key: str, model_name: str):
        self.api = api_key
        self.model = model_name
    
    def chat(self, prompt: str):
        print(f"Undergoing instructions from human: {prompt}")