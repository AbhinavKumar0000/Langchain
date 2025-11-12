import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')
    
template1 = PromptTemplate(
  template=" Write a detialed report on {topic}",
  input_variables=["topic"],
)

template2 = PromptTemplate(
  template=" write 5 line summary on the following text {text}",
  input_variables=["text"],
)

parser = StrOutputParser()

topic = "Artificial Intelligence"
report_prompt = template1.format(topic=topic)
report_response = model.generate_content(report_prompt)
report_text = report_response.text

summary_prompt = template2.format(text=report_text)
final_response = model.generate_content(summary_prompt)
print(final_response.text)