import google.generativeai as genai
from dotenv import load_dotenv
import os

# Disable safety settings
from google.generativeai.types import HarmCategory, HarmBlockThreshold
safety_settings={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

# Interface for Gemini API
class GeminiInterface:
    def __init__(self, model_name: str='gemini-1.5-pro', system_prompt: str=None):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_name = model_name
        self.system_prompt = system_prompt
        if self.system_prompt:
            self.set_system_prompt(self.system_prompt)
        else:
            self.model = genai.GenerativeModel(model_name)

    def set_system_prompt(self, prompt):
        self.model = genai.GenerativeModel(model_name=self.model_name, system_instruction=prompt)

    def streamify(self, iterator):
        def iterator_func():
            for item in iterator:
                yield item.text
        return iterator_func

    def generate(self, user_prompt, system_prompt=None, stream=True):
        '''
            # When streaming use as follows:
                for resp in gemini.generate("What is the meaning of life?"):
                    print(resp.text)
        '''
        if system_prompt:
            self.set_system_prompt(system_prompt)
        if stream:
            return self.streamify(self.model.generate_content(user_prompt, stream=stream, safety_settings=safety_settings))
        else:
            return self.model.generate_content(user_prompt, stream=False, safety_settings=safety_settings)

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