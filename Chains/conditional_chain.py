import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableLambda, RunnableBranch
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
import os


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


parser = StrOutputParser()


class Feedback(BaseModel):
  sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the feedback")


parser2 = PydanticOutputParser(pydantic_object=Feedback)


prompt1 = PromptTemplate(
  template="Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instruction}",
  input_variables=["feedback"],
  partial_variables={"format_instruction": parser2.get_format_instructions()} 
)


prompt2 = PromptTemplate(
  template="Write an appropriate response to the following positive feedback text \n {feedback}",
  input_variables=["feedback"]
)

prompt3 = PromptTemplate(
  template="Write an appropriate response to the following negative feedback text \n {feedback}",
  input_variables=["feedback"]
)


classifier_chain = prompt1 | model | parser2


branch_chain = RunnableBranch(
  (lambda x: x.sentiment == 'positive', prompt2 | model | parser),
  (lambda x: x.sentiment == 'negative', prompt3 | model | parser),
  RunnableLambda(lambda x: "Unable to determine sentiment."),
)

chain = classifier_chain | branch_chain

print(chain.invoke({"feedback": "I love the new features of your product!"}))

chain.get_graph().print_ascii()