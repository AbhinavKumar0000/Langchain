
from langchain_classic import hub
from langchain.agents import create_agent
from langchain_core.tools import tool, InjectedToolArg
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import requests
from typing import Annotated
load_dotenv()




@tool
def convert(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert amount and return formatted result with rate."""
    url = f'https://v6.exchangerate-api.com/v6/c754eab14ffab33112e380ca/pair/{from_currency}/{to_currency}'
    response = requests.get(url)
    data = response.json()
    rate = data.get('conversion_rate', 0)
    result = amount * rate
    return f"Rate: 1 {from_currency} = {rate:.4f} {to_currency}\n{amount} {from_currency} = {result:.4f} {to_currency}"



llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
prompt = hub.pull("hwchase17/react")

tools = [get_conversion_factor, convert]

app = create_agent(llm, tools)


user_query = "What is the conversion factor between INR and USD, and convert 10 INR to USD?"


for chunk in app.stream(
    {"messages": [("human", user_query)]},
    stream_mode="values",           # shows full state every step
    config={"recursion_limit": 15}  # ← config is a keyword argument
):
    if "messages" in chunk:
        msg = chunk["messages"][-1]
        if msg.type == "ai":
            print("ASSISTANT:", msg.content.strip())
            print("-" * 60)
        elif msg.type == "tool":
            print(f"TOOL → {msg.name}")
            print(f"RESULT → {msg.content}")
            print("-" * 60)

print("\nDONE")