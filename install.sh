#!/bin/bash
set -e

echo "Creating a virtual environment..."
python -m venv venv

echo "Activating the virtual environment..."

# Detect OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete!"
