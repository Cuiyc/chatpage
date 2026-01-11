#!/bin/bash

# YC Spark Chatbot Systemd Service Installer
# This script installs the chatbot as a systemd service

set -e

SERVICE_NAME="chatbot"
SERVICE_FILE="chatbot.service"
WORKING_DIR="/Users/cuiyc/workspace/chatpage"
USER="cuiyc"

echo "🚀 Installing YC Spark Chatbot as systemd service..."

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run this script with sudo privileges"
    echo "Usage: sudo $0"
    exit 1
fi

# Check if service file exists
if [ ! -f "$SERVICE_FILE" ]; then
    echo "❌ Service file '$SERVICE_FILE' not found!"
    exit 1
fi

# Check if working directory exists
if [ ! -d "$WORKING_DIR" ]; then
    echo "❌ Working directory '$WORKING_DIR' not found!"
    exit 1
fi

# Copy service file to systemd directory
echo "📋 Copying service file to /etc/systemd/system/..."
cp "$SERVICE_FILE" "/etc/systemd/system/$SERVICE_NAME.service"

# Reload systemd daemon
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

# Enable the service
echo "✅ Enabling service to start on boot..."
systemctl enable "$SERVICE_NAME"

echo ""
echo "🎉 Service installation complete!"
echo ""
echo "📋 Service Management Commands:"
echo "  Start service:   sudo systemctl start $SERVICE_NAME"
echo "  Stop service:    sudo systemctl stop $SERVICE_NAME"
echo "  Restart service: sudo systemctl restart $SERVICE_NAME"
echo "  Check status:    sudo systemctl status $SERVICE_NAME"
echo "  View logs:       sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "🌐 The chatbot will be accessible at: http://localhost:8501"
echo "   (assuming default Streamlit port)"
echo ""
echo "⚠️  Make sure your Ollama backend is running at http://spark:11434"
echo "   before starting the service."