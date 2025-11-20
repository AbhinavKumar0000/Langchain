from langchain_core.tools import BaseTool
from pydantic import BaseModel,Field
from typing import Type


class MultiplyInput(BaseModel):
    a: int = Field(required=True, description="first number")
    b: int = Field(required=True, description="second number")


class MultiplyTool(BaseTool):
    name: str = "Multiply"
    description: str = "Multiply two numbers"
    args_schema: Type[BaseModel]  = MultiplyInput


    def _run(self, a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b
    

multiply_tool = MultiplyTool()

result = multiply_tool.invoke({"a":3, "b":5})
print(result)

print(multiply_tool.name)
print(multiply_tool.description)  
print(multiply_tool.args)