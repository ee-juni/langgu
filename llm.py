import google.generativeai as genai
from dotenv import load_dotenv
import os

# Interface for Gemini API
class GeminiInterface:
    def __init__(self, model_name: str='gemini-1.5-flash', system_prompt: str=None):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_name = model_name
        self.system_prompt = system_prompt
        if self.system_prompt:
            self.set_system_prompt(self.system_prompt)
        else:
            self.model = genai.GenerativeModel(model_name)

    def set_system_prompt(self, prompt):
        self.model = genai.GenerativeModel(model_name=self.model_name, system_prompt=prompt)

    def generate(self, prompt, stream=True):
        '''
            # When streaming use as follows:
                for resp in gemini.generate("What is the meaning of life?"):
                    print(resp.text)
        '''
        return self.model.generate_content(prompt, stream=stream)
    
    def send_messages(self, messages: dict, stream: bool=True):
        '''
            Send messages (history + current message)
            Eg) messages = [
                {
                    "role": "user",
                    "parts": "What is the meaning of life?"
                },
                {
                    "role": "model",
                    "parts": "Pie"
                }, ...
            ]
        '''
        chat = self.model.start_chat(history=messages[:-1])
        return chat.send_message(messages[-1], stream=stream)


if __name__ == '__main__':
    gemini = GeminiInterface()
    for resp in gemini.generate("What is the meaning of life?"):
        print(resp.text)