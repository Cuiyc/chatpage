# Chatbot with OpenAI Compatible Backend

This is a Streamlit-based chatbot application that connects to an OpenAI-compatible backend (such as Ollama) to provide conversational AI capabilities.

## Features

- Streamlit UI for chat interface
- Dynamic model listing from backend
- Default model selection (qwen3-coder-30b-32k:latest)
- Session-based conversation memory
- Responsive chat interface

## Requirements

- Python 3.7+
- Streamlit
- Requests
- OpenAI Python library

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

## Project Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies

## Configuration

The application connects to `http://spark:11434/v1/models` by default. You can modify this URL in the code if your backend is hosted elsewhere.

## Notes

- The application will fetch available models from the backend on each page load
- Conversations are stored in session state
- The default model is set to `qwen3-coder-30b-32k:latest`