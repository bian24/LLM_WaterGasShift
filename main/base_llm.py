import json
import os
import requests
from openai import OpenAI

LLM_MODEL = os.getenv("LLM_MODEL")


class BaseLLM:
    def __init__(self):
        self.llm = LLM_MODEL
        
    
    def generate_answer(self, query):
        """
        Generate answer using base llms
        """
        if "llama" in self.llm:
            self.url = 'http://localhost:11434/api/generate'
            self.payload = None
            self.payload = {
                "model": LLM_MODEL,
                "prompt": query
            }
            data = json.dumps(self.payload)

            response = requests.post(self.url, data=data, headers={'Content-Type': 'application/json'})
            list_dict_words = []
            for each_word in response.text.split("\n"):
                try:
                    data = json.loads(each_word) 
                except:
                    pass
                list_dict_words.append(data)
                    
            answer = " ".join([word['response'] for word in list_dict_words if type(word) == type({})])
           
        elif "gpt" in self.llm:
            client = OpenAI()
            completion = client.chat.completions.create(
                model = self.llm,
                messages = [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            )

            answer = completion.choices[0].message.content
        
        else:
            answer = "no llm selected"
        
        return answer