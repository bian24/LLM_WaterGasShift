import requests
import json

class llama:
    def __init__(self):
        self.url = 'http://localhost:11434/api/generate'
        self.payload = None
    
    def generate_answer_llama(self, query):
        """
        Generate answer using local llama
        """
        self.payload = {
            "model": "llama3.2",
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
                
        llama_response = " ".join([word['response'] for word in list_dict_words if type(word) == type({})])
        
        return llama_response