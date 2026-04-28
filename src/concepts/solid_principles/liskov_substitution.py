from os import environ

# Custom modules
from llm_objects import ChatGPT

# SRP - retrieve_api_key
def retrieve_api_key(api_env_name: str) -> str:
    # Start the api_key by being None
    api_key = ""

    # Check whether API key is there
    if api_env_name in environ:
        api_key = environ.get(key=api_env_name, default="")
    
    else:
        raise ValueError("The API key is missing.")
    
    return api_key

# Liskov Substitution Principle
def load_model(model_name: str, api_env_name: str) -> ChatGPT:

    api_key = retrieve_api_key(api_env_name=api_env_name)
    
    # ChatGPT Object
    chatgpt_obj = ChatGPT(api_key=api_key, model_name=model_name)

    return chatgpt_obj
    
    

