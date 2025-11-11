import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')


schema = [
  ResponseSchema(name="fact1", description="The first fact about the topic"),
  ResponseSchema(name="fact2", description="The second fact about the topic"),
  ResponseSchema(name="fact3", description="The third fact about the topic"),
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template='Give me 3 facts about {topic} \n {format_instruction}',
    input_variables=['topic'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

topic = "Black hole"
report_prompt = template.format(topic=topic)
report_response = model.generate_content(report_prompt)
report_text = parser.parse(report_response)

print(report_text)
