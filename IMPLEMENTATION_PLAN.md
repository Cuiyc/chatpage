# Implementation Plan: Add Search Tool to Chatbot

## Overview
Add DuckDuckGo search functionality to the chatbot using LangGraph and LangChain's DuckDuckGo integration.

## Files to Create/Modify

### 1. requirements.txt
**Changes:** Add dependencies:
- `langchain`
- `langchain-community`
- `langgraph`
- `duckduckgo-search`

### 2. tools.py (NEW)
**Purpose:** Implement the search tool
- Create DuckDuckGoSearchRun instance
- Format search results for LLM consumption
- Return structured results with URLs, titles, and snippets

### 3. agent.py (NEW)
**Purpose:** LangGraph agent workflow
- Define tool schema for search
- Create LangGraph state with messages and tools
- Model node: calls LLM with tools
- Tool node: executes search when needed
- Conditional routing between model and tool nodes
- Initialize with OpenAI client from Ollama

### 4. app.py (MODIFY)
**Changes:**
- Import agent module
- Replace direct model call with LangGraph agent
- Handle tool calls and display search results
- Add visual distinction for search results
- Show search indicator when tool is used
- Keep existing session state management

## Implementation Steps

1. Update dependencies in requirements.txt
2. Create tools.py with DuckDuckGo search implementation
3. Create agent.py with LangGraph workflow
4. Modify app.py to integrate the agent
5. Test the implementation

## UI Changes
- Add indicator when search is used
- Display search results separately with formatting
- Maintain existing chat interface
