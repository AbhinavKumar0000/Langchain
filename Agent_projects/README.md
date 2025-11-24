#  Smart Currency Agents with LangChain & Gemini 2.0

This repository demonstrates two advanced patterns for building AI Agents using LangChain and Google Gemini 2.0 Flash. It solves a real-world problem—retrieving live exchange rates and performing conversions—using two different architectural approaches.





##  Approach 1: The Autonomous ReAct Agent

**File:** `autonomous_agent.py`

This script uses the classic ReAct (Reason + Act) pattern. The LLM is given a list of tools and a goal. It autonomously decides which tool to call and when.

### Key Features:

* **Model**: `gemini-2.0-flash` (High speed)
* **Framework**: Uses `langchain.agents` and `hub.pull("hwchase17/react")`
* **Streaming**: Implements full state streaming to visualize the agent's thought process in real-time

### How It Works:

1. LLM decides which tool to call (`get_conversion_factor`)
2. Observes the output
3. Decides to call the next tool (`convert`) or answer the user

##  Approach 2: Tool Injection & State Management

**File:** `injected_tool_agent.py`

This script demonstrates a Senior Engineering pattern called `InjectedToolArg`. Instead of letting the LLM "guess" or "read" the rate from a chat string, we programmatically inject the precise data from the first tool into the second tool.

### Why this is better for production:

* **Safety**: The `conversion_rate` argument in the convert function is `Annotated` with `InjectedToolArg`. The LLM cannot hallucinate this number; the code must provide it.
* **Control**: We manually handle the execution flow (Step 1 → Step 2), ensuring precise data passing.

```python
# The Magic of Injection
@tool
def convert(base_value: float, rate: Annotated[float, InjectedToolArg]) -> float:
    # The LLM provides 'base_value', but Python code provides 'rate'
    return base_value * rate
