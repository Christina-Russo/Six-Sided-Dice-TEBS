#! /bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Install needed modules
pip install fastapi[standard] requests pynput &&
# Install node_modules for frontend
cd frontend/interactive-system && npm install && npm run build
