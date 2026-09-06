#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=================================================="
echo "ROCmForge: Starting Automated Setup Engine"
echo "=================================================="

# 1. Check if Python 3 is installed on the system
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed on this system."
    echo "Please install Python 3 and try running this script again."
    exit 1
fi

echo "Python 3 detected successfully."

# 2. Check for or create the Python Virtual Environment (.venv)
if [ ! -d ".venv" ]; then
    echo "Creating isolated Python virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "Existing virtual environment (.venv) found. Skipping creation."
fi

# 3. Determine the correct platform-specific activation path
if [ -d ".venv/bin" ]; then
    ACTIVATE_PATH=".venv/bin/activate"
elif [ -d ".venv/Scripts" ]; then
    ACTIVATE_PATH=".venv/Scripts/activate"
else
    echo "Error: Could not locate the virtual environment activation script structure."
    exit 1
fi

# 4. Activate the virtual environment
echo "Activating the virtual environment..."
source "$ACTIVATE_PATH"

# 5. Upgrade package management core tools
echo "Upgrading pip, setuptools, and wheel packages..."
pip install --upgrade pip setuptools wheel

# 6. Check for requirements.txt and install library dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing required framework dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt could not be found. Skipping package installations."
fi

echo "=================================================="
echo "ROCmForge Setup Completed Successfully! "
echo "=================================================="
echo "To activate your environment in the terminal, run:"
echo "   source $ACTIVATE_PATH"
echo "To run the agent pipeline execution test, run:"
echo "   python src/main.py sample_legacy_cuda.py"
echo "=================================================="
