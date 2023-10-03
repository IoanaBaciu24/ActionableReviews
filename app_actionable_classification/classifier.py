"""Module responsible for classifying wether a review contains an actionable part"""
from abc import ABC, abstractmethod
from typing import Any
from langchain.pydantic_v1 import BaseModel, Field
from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_structured_output_chain,
)
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, PromptTemplate


SYSTEM = """You are a classifer for actionable reviews. A review is actionable if it contains any information that can be used to improve the app."""
EXAMPLES= """Here are some examples you can follow:
```
Classify the following review: Why showing notification even when I completed the task for keeping the streak, it's irritating
Answer(actionable=True)

Classify the following review: wow this is amazing
Answer(actionable=False)

Classify the following review: It is nice but I have to give it 1 star because you just can't set your profile photo, i don't want to set my avatar and now you can't even see other people's profile photo, this is really very embarrassing pls fix this
Answer(actionable=True)

Classify the following review: I don't like this version it is horrible it's really hard I don't like the stepping stones
Answer(actionable=False)

Classify the following review:It's heavy and it crashes a lot after the last update. Almost unusable. Edit: And now all the new lessons in the Czech language have disappeared after the new interface was introduced. I keep getting the same exercises in endless "personalized practice". No new lessons, nothing, only endless personalized practices. Please fix it.
Answer(actionable=True)

Classify the following review: bad 😞
Answer(actionable=False)
```
"""
ACTIONABLE_DESCRIPTION = """True if the review is actionable, False otherwise."""


class Answer(BaseModel):
    """Answer format"""
    actionable: bool = Field(..., description=ACTIONABLE_DESCRIPTION)

class ActionableReviewClassifier(ABC):
    """Base class for the classifiers"""
    @abstractmethod
    def __call__(self, review: str) -> bool:
        pass


class ActionableReviewClassifierChat(ActionableReviewClassifier):
    """Classifier for reviews, uses chat models"""
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model, temperature=0)
      

    def __call__(self, review: str) -> bool:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM ),
                ("human", "Classify the following review: {review}"),
                ("human", "Tip: Make sure to answer in the correct format"),
                ("human", EXAMPLES)
            ]
        )
        chain = create_structured_output_chain(Answer, self.llm, prompt, verbose=True)
        response = chain.run(review)
        return response.actionable


class ActionableReviewClassifierInstructLLM(ActionableReviewClassifier):
    """Classifier for reviews, compaible with non-chat models"""
    def __init__(self, model: str = "gpt-3.5-turbo-instruct"):
        self.llm = OpenAI(model=model, temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=Answer)

    def __call__(self, review: str) -> bool:
        template = PromptTemplate(
            template=SYSTEM + "\n{format_instructions}.\n" + EXAMPLES + \
                "\nClassify the following review: {review}",
            input_variables=["review"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},)
        prompt = template.format_prompt(review=review).to_string()
        output = self.llm(prompt)
        # Ok so this is a very ugly hack. Normally I would try to format the output as a json,
        # to have structured output, but this is just a small pet project
        try: 
            return eval(output.strip()).actionable
        except:
            print(output)
            if "True" in output:
                return True
            return False
