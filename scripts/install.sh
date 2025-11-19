#!/bin/bash
set -e

echo "Installing ThoughtStream..."

# Check for Python 3.10+
python3 --version

# Create venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
pip install -e .

# Setup config
mkdir -p ~/.config/thoughtstream
if [ ! -f ~/.config/thoughtstream/config.yaml ]; then
    cp config.yaml.example ~/.config/thoughtstream/config.yaml
fi

# Systemd setup (Linux only)
if [ -d "/etc/systemd" ]; then
    # Create service file...
    echo "Systemd setup skipped for now."
fi

echo "Installation complete. Run 'thoughtstream daemon' to start."

