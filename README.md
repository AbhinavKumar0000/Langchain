# LangChain Learning Journey & Projects

This repository documents my comprehensive journey learning LangChain through hands-on implementation of various concepts, patterns, and real-world applications. Each directory represents a specific learning module with practical code examples.

##  Learning Path Structure

###  Core Concepts

#### 1. **Chains** - Building Processing Pipelines
- `simple_chain.py`: Basic sequential chain implementation
- `parallel_chain.py`: Running multiple chains concurrently
- `conditional_chain.py`: Dynamic chain routing based on conditions

#### 2. **Data Loaders** - Handling Various Data Sources
- `loader.py`: Unified data loading for multiple formats
- Supported formats: CSV (`Social_Network_Ads.csv`), PDF (`pdf_sample.pdf`), Text (`one_piece.txt`)

#### 3. **Parsers** - Structured Output Processing
- `str_output_parser.py`: Basic string parsing
- `Json_output_parser.py`: JSON response formatting
- `pydantic_output_parser.py`: Type-safe parsing with Pydantic
- `structured_output_parser.py`: Complex structured data handling
- `typedef.py`: Type definitions and utilities

#### 4. **Runnables** - Composable Operations
- `runnable_sequence.py`: Sequential execution flows
- `runnable_parallel.py`: Parallel task execution
- `runnable_branch.py`: Conditional routing
- `runnable_lambda.py`: Custom function integration
- `runnable_passthrough.py`: Data forwarding utilities

### 🔧 Tools & Custom Functionality

#### 5. **Custom Tools** - Extending LangChain Capabilities
- `BaseTool_class.py`: Foundation for custom tool creation
- `structured_tool.py`: Type-validated tools
- `@tool_type.py`: Decorator-based tool definitions
- `custom_toolkit.py`: Bundled tool collections

#### 6. **Tool Calling** - Advanced Tool Integration
- `tool_binding.py`: Dynamic tool attachment and invocation

#### 7. **Pre-built Tools** - Ready-to-Use Utilities
- `cmd.py`: Command-line execution tools
- `duck.py`: DuckDuckGo search integration

###  Retrieval Systems

#### 8. **Retrievers** - Information Fetching Strategies
- `vector_store_retriever.py`: Dense vector-based retrieval
- `MMR_retriever.py`: Maximum Marginal Relevance for diversity
- `MOR_retriever.py`: Multi-Query Retrieval
- `contextual_compression_retriev...`: Compressed context retrieval
- `wikipedia_retriever.py`: Wikipedia-specific retrieval

#### 9. **Database** - Vector Storage Solutions
- `chroma_setup.py`: ChromaDB vector database configuration
- `my_chroma_db/`: Persistent vector storage with SQLite

##  Featured Projects

### Project 1: **RAGTube** - Chat with YouTube Videos
**Location:** `Project_ytchatbot/`

A full-stack application that enables conversational interactions with YouTube video content using RAG (Retrieval-Augmented Generation).

#### Key Features:
- YouTube transcript extraction and processing
- FAISS vector store for semantic search
- Google Gemini integration for intelligent responses
- Flask-based web interface with dark mode UI
- Real-time chat experience



### Project 2: **Smart Currency Agents**
**Files:** `currency_convert_agent.py`, `curresy_convert_agent.py`

Two distinct approaches to building currency conversion agents demonstrating different architectural patterns.

#### Approach 1: Autonomous ReAct Agent
- Self-directed tool usage and reasoning
- Real-time thought process streaming
- Dynamic decision making

#### Approach 2: Injected Tool Flow
- Programmatic data injection between tools
- Controlled execution flow
- Prevention of number hallucination

##  Technical Stack

- **Framework**: LangChain, LangChain Community
- **LLM**: Google Gemini 2.0 Flash
- **Vector DB**: ChromaDB, FAISS
- **Web Framework**: Flask
- **Data Processing**: Pydantic, Various parsers
- **Tools**: Custom tools, Command line, Web search

##  Learning Methodology

### Hands-On Implementation
Each concept was learned through:
1. **Theory Understanding**: Studying LangChain documentation and tutorials
2. **Code Implementation**: Building working examples for each pattern
3. **Project Integration**: Combining multiple concepts into real applications
4. **Optimization**: Refining implementations based on performance and best practices

### Progressive Complexity
- Started with basic chains and parsers
- Advanced to custom tools and complex retrievers
- Built complete applications integrating multiple concepts
- Implemented production-ready patterns like injected tool flows

##  Key Learnings

### 1. **Chain Composition**
- Sequential, parallel, and conditional chaining
- Error handling in complex workflows
- State management across chain steps

### 2. **Retrieval Optimization**
- Vector similarity search techniques
- Context compression strategies
- Multi-query retrieval for better coverage

### 3. **Tool Integration**
- Custom tool creation with proper typing
- Dynamic tool binding and invocation
- Safe tool execution patterns

### 4. **Production Patterns**
- Injected tool arguments for data safety
- Structured output parsing for reliability
- Efficient vector storage and retrieval



##  Reference Materials

### Primary Learning Resource
- **YouTube Playlist**: [LangChain Project Playlist by Krish Naik](https://www.youtube.com/watch?v=pSVk-5WemQ0&list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- **Repository**: [Original Learning Code](https://github.com/AbhinavKumar0000/Langchain/tree/main)

### Additional Resources
- LangChain Official Documentation
- Google Gemini API Documentation
- Various AI/ML communities and forums

---

**Developer**: Abhinav Kumar  
**Learning Period**: Comprehensive LangChain mastery  
**Status**: Continuously updating with new patterns and projects
