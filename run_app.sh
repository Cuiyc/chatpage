#!/bin/bash

# Run the Streamlit chatbot application
echo "Starting Streamlit chatbot application..."
echo "Make sure your OpenAI-compatible backend is running at http://spark:11434"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

./venv/bin/python -m streamlit run app.py