#! /bin/bash

echo "Running DirtBag Pi in the background"
source venv/bin/activate
nohup python3 api/app.py &

