# Chatbot with OpenAI Compatible Backend

This is a Streamlit-based chatbot application that connects to an OpenAI-compatible backend (such as Ollama) to provide conversational AI capabilities with web search functionality.

## Features

- Streamlit UI for chat interface
- Dynamic model listing from backend
- Default model selection (qwen3-coder-30b-32k:latest)
- Session-based conversation memory
- Responsive chat interface
- **Web search integration** using DuckDuckGo via LangGraph
- **Intelligent tool calling** - LLM automatically decides when to search the web
- **Visual search indicators** - Search queries and results are clearly displayed in chat

## Requirements

- Python 3.7+
- Streamlit
- Requests
- OpenAI Python library
- LangChain
- LangGraph
- LangChain Community
- DuckDuckGo Search
- ddgs

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure your OpenAI-compatible backend is running (e.g., Ollama server on http://spark:11434)
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. The application will be accessible at http://localhost:8501/chat
4. Select a model from the sidebar
5. Start chatting!

### Using Web Search

The chatbot can now automatically search the web when needed. Simply ask questions that require current information:

- "What's the latest news about AI?"
- "Who won the NBA championship last year?"
- "What's the current price of Bitcoin?"

The LLM will automatically detect when web search is needed and display:
- 🔍 Search queries being executed
- 📄 Search results with snippets

Search results are formatted and displayed separately from the main response.

## Project Structure

- `app.py` - Main Streamlit application
- `agent.py` - LangGraph agent workflow with tool integration
- `tools.py` - DuckDuckGo search tool implementation
- `requirements.txt` - Python dependencies
- `IMPLEMENTATION_PLAN.md` - Implementation plan for search feature

## Configuration

The application connects to `http://spark:11434/v1/models` by default. You can modify this URL in the code if your backend is hosted elsewhere.

## Architecture

The chatbot uses a LangGraph-based agent architecture:

1. **User Input** → Messages are sent to the LangGraph agent
2. **Agent Node** → LLM processes the message and decides whether to use tools
3. **Tool Routing** → If the LLM decides to search, it routes to the tool node
4. **Tool Execution** → DuckDuckGo search is performed and results are returned
5. **Final Response** → LLM generates a response based on search results if available

The agent workflow:
- Uses `ChatOpenAI` with tool binding for function calling
- Conditional routing between model and tool nodes
- Automatic tool invocation based on LLM decision
- State management through LangGraph's state system

## Notes

- The application will fetch available models from the backend on each page load
- Conversations are stored in session state
- The default model is set to `qwen3-coder-30b-32k:latest`
- Web search is automatically invoked by the LLM when it detects the need for current information
- Search results are displayed with visual indicators for clarity