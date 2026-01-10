import streamlit as st
import requests
import json
from openai import OpenAI
from typing import List, Dict, Any

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "qwen3-coder-30b-32k:latest"
if "models" not in st.session_state:
    st.session_state.models = []

# App title
st.title("Chat with OpenAI Compatible Backend")

# Sidebar for model selection
with st.sidebar:
    st.header("Settings")
    
    # Fetch models from backend
    try:
        response = requests.get("http://spark:11434/v1/models", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            st.session_state.models = [model["id"] for model in models_data.get("data", [])]
        else:
            st.warning("Failed to fetch models from backend")
            # Fallback to a default list
            st.session_state.models = ["qwen3-coder-30b-32k:latest", "gpt-3.5-turbo", "gpt-4"]
    except Exception as e:
        st.warning(f"Error fetching models: {str(e)}")
        # Fallback to a default list
        st.session_state.models = ["qwen3-coder-30b-32k:latest", "gpt-3.5-turbo", "gpt-4"]
    
    # Model selection
    selected_model = st.selectbox(
        "Select Model",
        options=st.session_state.models,
        index=st.session_state.models.index(st.session_state.selected_model) if st.session_state.selected_model in st.session_state.models else 0
    )
    
    st.session_state.selected_model = selected_model
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is your message?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from backend
    try:
        # Initialize OpenAI client with the selected model
        client = OpenAI(
            base_url="http://spark:11434/v1",
            api_key="ollama"  # Ollama doesn't require an API key
        )
        
        # Get response from the model
        response = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True
        )
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        # Add error message to chat history
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})