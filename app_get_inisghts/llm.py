"""LLM wrapper"""
from typing import List
import json
import openai

class LLM:
    def __init__(self, prompt_template: str, model:str="gpt-3.5-turbo", temperature:float=0):
        self.template = prompt_template
        self.model = model
        self.temperature = temperature

    def format_prompt(self, reviews: List[str]) -> str:
        """Function creates the prompt from the template and reviews list"""
        print(len(reviews))
        return self.template.format(reviews="\n".join(reviews))
    
    def process_output(self, llm_response):
        try:
            start_index = llm_response.find('{') + 1
            end_index = llm_response.find('}', start_index)
            json_text = llm_response[start_index:end_index]
            result = json.loads(json_text)
            result["postprocessing_successful"] = True
            result["raw_text"] = llm_response
            return result
        except:
            print("Problem decoding:\n", llm_response)
            return {"postprocessing_successful": False, "raw_text": llm_response}
    
    def __call__(self, reviews: List[str]) -> str:
        le_prompt = self.format_prompt(reviews)
        messages  = [
            {"role":"system", "content":"You are a useful text summarizer, with an affinity to finding actionable insights in the text you analyze."},
            {"role":"user", "content":le_prompt}
            ]
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            llm_response = completion.choices[0].message["content"]
        except:
            print("Problem with")
            print(le_prompt)
            llm_response = ""
        return llm_response
