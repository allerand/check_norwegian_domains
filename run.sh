#!/bin/bash

echo "Activating virtual environment..."

source venv/bin/activate

echo "Installing dependencies..."

pip install -r requirements.txt

echo "Running script..."

python main.py 2>&1

echo "Deactivating virtual environment..."

deactivate

echo "Done."