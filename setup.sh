#!/usr/bin/env bash

set -e

echo "Creating virtual environment..."
if [ -x ".venv/bin/python" ] && [ "$(.venv/bin/python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')" != "3.11" ]; then
    echo "Existing virtual environment uses an unsupported Python version; recreating it with Python 3.11."
    rm -rf .venv
fi
if [ ! -x ".venv/bin/python" ]; then
    python3.11 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Validating installed UI and test dependencies..."
python -c "import PySide6, moderngl, pytest; print('PySide6, moderngl, and pytest are available.')"

echo ""
echo "Setup complete!"
echo ""
echo "Activate with:"
echo "source .venv/bin/activate"