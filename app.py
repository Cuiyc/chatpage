import streamlit as st
import requests
import json
from openai import OpenAI
from typing import List, Dict, Any
from langchain_core.messages import AIMessage, ToolMessage
from agent import create_graph, run_agent

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "qwen3-coder-30b-32k:latest"
if "models" not in st.session_state:
    st.session_state.models = []
if "show_thoughts" not in st.session_state:
    st.session_state.show_thoughts = True

# App title
st.title("YC Spark Demo")

# Sidebar for model selection
with st.sidebar:
    st.header("Settings")

    # Fetch models from backend
    try:
        response = requests.get("http://spark:11434/v1/models", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            st.session_state.models = [
                model["id"] for model in models_data.get("data", [])
            ]
        else:
            st.warning("Failed to fetch models from backend")
            # Fallback to a default list
            st.session_state.models = [
                "qwen3-coder-30b-32k:latest",
                "gpt-3.5-turbo",
                "gpt-4",
            ]
    except Exception as e:
        st.warning(f"Error fetching models: {str(e)}")
        # Fallback to a default list
        st.session_state.models = [
            "qwen3-coder-30b-32k:latest",
            "gpt-3.5-turbo",
            "gpt-4",
        ]

    # Model selection
    selected_model = st.selectbox(
        "Select Model",
        options=st.session_state.models,
        index=st.session_state.models.index(st.session_state.selected_model)
        if st.session_state.selected_model in st.session_state.models
        else 0,
    )

    st.session_state.selected_model = selected_model

    # Toggle for showing thoughts
    st.session_state.show_thoughts = st.checkbox("Show Thinking Steps", value=True)

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # If it's a thinking model response, we might want to display thoughts separately
        if message["role"] == "assistant" and "thoughts" in message:
            # Display the main response
            st.markdown(message["content"])
            # Display thoughts if enabled
            if st.session_state.show_thoughts:
                st.markdown("---")
                st.markdown("**Thinking Steps:**")
                for thought in message["thoughts"]:
                    st.markdown(f"- {thought}")
        else:
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is your message?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from backend using LangGraph agent
    try:
        graph = create_graph(
            model_name=st.session_state.selected_model, base_url="http://spark:11434/v1"
        )

        # Run the agent
        messages = st.run_sync(run_agent(graph, prompt, st.session_state.messages[:-1]))

        # Process and display messages
        assistant_messages = []
        search_results = []

        for msg in messages:
            if isinstance(msg, AIMessage):
                if msg.content:
                    assistant_messages.append(msg.content)
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        search_results.append(
                            f"🔍 **Search:** {tool_call['args'].get('query', 'N/A')}"
                        )
            elif isinstance(msg, ToolMessage):
                search_results.append(f"📄 **Results:** {msg.content[:200]}...")

        # Display assistant response
        with st.chat_message("assistant"):
            if search_results:
                st.markdown("---")
                for result in search_results:
                    st.markdown(result)
                st.markdown("---")

            full_response = " ".join(assistant_messages)
            message_placeholder = st.empty()
            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        # Add error message to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": f"Error: {str(e)}"}
        )
