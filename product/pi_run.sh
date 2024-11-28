#! /bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
# On exit, terminate all processes started from this script
trap 'kill -SIGINT 0' EXIT INT SIGTERM SIGINT 
# Start VE
source pi_venv/bin/activate
# Run server on 127.0.0.1:8000
pushd backend && uvicorn server:app --host 127.0.0.1 --port 8000 2> /dev/null && popd &
# Run frontend display w/o opening web browser
sleep 1 && npm run pi --prefix frontend/interactive-system &
# Run web browser in kiosk mode (fullscreen)
sleep 2 && chromium --app=http://localhost:5173 --kiosk &> /dev/null &
# Run application in VE
sleep 2 && sudo pi_venv/bin/python3 app.py
# Once application finishes, exit VE
deactivate