# Without Dependency Inversion
class LLM:
    def __init__(self) -> None:
        self.model_name = None

class ChatGPT:
    def __init__(self, model_name: str, api_key: str) -> None:
        # Attributes
        self.model_name = LLM()

        self.model_name.model_name = model_name


# With Dependency Inversion
class LLM:
    def __init__(self) -> None:
        self.model_name = None

    def wrong_method(self) -> None:
        return 5


class ChatGPT(LLM):
    def __init__(self, model_name: str, api_key: str) -> None:
        
        # Get everything that belongs to LLM
        super().__init__()

        # Attributes
        self.model_name = model_name
        self.api_key = api_key


# Example
chatgpt = ChatGPT(model_name='gpt-5', api_key='test_api')

print(chatgpt)

print(chatgpt.model_name)
print(chatgpt.api_key)
