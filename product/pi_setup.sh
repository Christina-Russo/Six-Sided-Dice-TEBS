#! /bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Setup Virtual environment
python3 -m venv pi_venv
# Install needed modules in VE
pi_venv/bin/pip3 install fastapi[standard] requests pynput rpi-gpio
# Install node if needed
sudo apt install npm -y
# Install node_modules for frontend
cd frontend/interactive-system && npm install && npm run build
cd "$parent_path"