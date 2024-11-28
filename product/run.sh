#! /bin/bash
parent_path="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"
cd "$parent_path"

# On exit, terminate all processes started from this script
trap 'kill -SIGINT 0' EXIT INT SIGTERM SIGINT
# Run server on 127.0.0.1:8000
pushd backend && uvicorn server:app --host 127.0.0.1 --port 8000 2> /dev/null && popd &
# Run frontend display
npm run dev &> /dev/null --prefix frontend/interactive-system &
# Run application
python app.py #2> /dev/null