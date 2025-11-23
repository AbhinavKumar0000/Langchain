from langchain_core.tools import tool, InjectedToolArg
from langchain_core.messages import HumanMessage
import requests
from typing import Annotated
import json


from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()



@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
  """
  This function fetches the currency conversion factor between a given base currency and a target currency
  """
  url = f'https://v6.exchangerate-api.com/v6/c754eab14ffab33112e380ca/pair/{base_currency}/{target_currency}'

  response = requests.get(url)

  return response.json()

@tool
def convert(base_currency_value: float, conversion_rate: Annotated[float, InjectedToolArg]) -> float:
  """
  given a currency conversion rate this function calculates the target currency value from a given base currency value
  """

  return base_currency_value * conversion_rate



llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

llm_with_tools = llm.bind_tools([get_conversion_factor, convert])
messages = [HumanMessage('What is the conversion factor between INR and USD, and based on that can you convert 10 inr to usd')]


ai_msg_1 = llm_with_tools.invoke(messages)
messages.append(ai_msg_1)

current_conversion_rate = None

if ai_msg_1.tool_calls:
    for tool_call in ai_msg_1.tool_calls:
        if tool_call['name'] == 'get_conversion_factor':
            print(f"-> Step 1: Calling {tool_call['name']}")
            
            tool_output = get_conversion_factor.invoke(tool_call)
            
            data = json.loads(tool_output.content)
            current_conversion_rate = data['conversion_rate']
            
            messages.append(tool_output)

ai_msg_2 = llm_with_tools.invoke(messages)
messages.append(ai_msg_2)

if ai_msg_2.tool_calls:
    for tool_call in ai_msg_2.tool_calls:
        if tool_call['name'] == 'convert':
            print(f"-> Step 2: Calling {tool_call['name']}")
            
            tool_call['args']['conversion_rate'] = current_conversion_rate
            
            tool_output = convert.invoke(tool_call)
            messages.append(tool_output)


print(llm_with_tools.invoke(messages).content)