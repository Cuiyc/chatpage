#!/bin/bash

# YC Spark Chatbot Service Debug Script
# Run this to diagnose common service issues

echo "🔍 Debugging YC Spark Chatbot Service"
echo "======================================"

echo -e "\n=== Service Status ==="
sudo systemctl status chatbot --no-pager -l 2>/dev/null || echo "❌ Service not installed or not running"

echo -e "\n=== Recent Logs ==="
sudo journalctl -u chatbot -n 10 --no-pager 2>/dev/null || echo "❌ No logs available (service may not be installed)"

echo -e "\n=== Environment Check ==="
sudo -u cuiyc bash -c 'echo "User: $(whoami)"; echo "Dir: $(pwd)"; echo "Python: $(python --version 2>&1)"; echo "Streamlit: $(which streamlit || echo Not found)"' 2>/dev/null || echo "❌ Cannot check environment as cuiyc user"

echo -e "\n=== Virtual Environment Check ==="
if [ -f "/Users/cuiyc/workspace/chatpage/venv/bin/python" ]; then
    echo "✅ Virtual environment found"
    sudo -u cuiyc bash -c 'echo "Venv Python: $(/Users/cuiyc/workspace/chatpage/venv/bin/python --version 2>&1)"' 2>/dev/null
else
    echo "❌ Virtual environment not found at /Users/cuiyc/workspace/chatpage/venv/"
fi

echo -e "\n=== Dependency Check ==="
sudo -u cuiyc bash -c 'cd /Users/cuiyc/workspace/chatpage 2>/dev/null && ./venv/bin/python -c "
try:
    import streamlit, langchain, langgraph, duckduckgo_search
    print(\"✅ All Python dependencies OK\")
except ImportError as e:
    print(f\"❌ Import error: {e}\")
"' 2>/dev/null || echo "❌ Cannot check dependencies"

echo -e "\n=== Ollama Backend Check ==="
if curl -s http://spark:11434/v1/models > /dev/null 2>&1; then
    echo "✅ Ollama backend responding"
else
    echo "❌ Ollama backend not responding on http://spark:11434"
fi

echo -e "\n=== File Permissions Check ==="
if [ -f "/Users/cuiyc/workspace/chatpage/run_app.sh" ]; then
    ls -la /Users/cuiyc/workspace/chatpage/run_app.sh
    if [ -x "/Users/cuiyc/workspace/chatpage/run_app.sh" ]; then
        echo "✅ run_app.sh is executable"
    else
        echo "❌ run_app.sh is not executable"
    fi
else
    echo "❌ run_app.sh not found"
fi

echo -e "\n=== Port Check ==="
if sudo lsof -i :8501 > /dev/null 2>&1; then
    echo "❌ Port 8501 is already in use:"
    sudo lsof -i :8501
else
    echo "✅ Port 8501 is free"
fi

echo -e "\n=== Service File Check ==="
if [ -f "/etc/systemd/system/chatbot.service" ]; then
    echo "✅ Service file exists"
    sudo systemd-analyze verify /etc/systemd/system/chatbot.service 2>&1 || echo "❌ Service file has syntax errors"
else
    echo "❌ Service file not found in /etc/systemd/system/"
fi

echo -e "\n📋 Quick Fix Commands:"
echo "  Fix permissions: chmod +x /Users/cuiyc/workspace/chatpage/run_app.sh"
echo "  Reload systemd: sudo systemctl daemon-reload"
echo "  Restart service: sudo systemctl restart chatbot"
echo "  Check status: sudo systemctl status chatbot"
echo "  View logs: sudo journalctl -u chatbot -f"