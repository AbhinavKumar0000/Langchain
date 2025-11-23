from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiplies two numbers and returns the result."""
    return a * b


querry = HumanMessage("Can you Multiply 6 by 7")
message = [querry]
llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.1)

llm_with_tools = llm.bind_tools([multiply_numbers])

response = llm_with_tools.invoke("Can you Multiply 6 by 7")

message.append(response)


tool_result = multiply_numbers.invoke(response.tool_calls[0])

message.append(tool_result)

print(llm_with_tools.invoke(message).content)

