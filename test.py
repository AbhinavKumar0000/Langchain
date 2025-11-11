import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')

class Person(BaseModel):
  name: str = Field(description="Name of the person")
  age: int = Field(gt=18, description="Age of the person")
  city: str = Field(description="City name of the person belongs to")


parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
  template = "Generate the name, age and city of a fictional {place} person \n {format_instruction}",
  input_variables=['place'],
  partial_variables={'format_instruction': parser.get_format_instructions()}
)

placew = "india"
prompt = template.format(place=placew)
report_response = model.generate_content(prompt)
print(report_response.text)

