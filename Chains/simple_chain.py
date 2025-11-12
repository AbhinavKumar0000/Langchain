import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import Runnable, RunnableBranch
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
import os


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


parser = StrOutputParser()


class Feedback(BaseModel):
  sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the feedback")


parser2 = PydanticOutputParser(pydantic_object=Feedback)


prompt1 = PromptTemplate(
  template="Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instruction}",
  input_variables=["feedback"],
  partial_variables={"format_instruction": parser2.get_format_instructions()} 
)



classifier_chain = prompt1 | model | parser2

result = classifier_chain.invoke({"feedback": "this is terrible smartphone"}).sentiment
print(result)