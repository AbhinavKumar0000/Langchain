from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()



@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiplies two numbers and returns the result."""
    return a * b


querry = HumanMessage("Can you Multiply 6 by 7")
message = [querry]
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

llm_with_tools = llm.bind_tools([multiply_numbers])

response = llm_with_tools.invoke("Can you Multiply 6 by 7")

message.append(response)


tool_result = multiply_numbers.invoke(response.tool_calls[0])

message.append(tool_result)

print(llm_with_tools.invoke(message).content)

