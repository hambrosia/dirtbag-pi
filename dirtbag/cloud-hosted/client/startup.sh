#! /bin/bash

echo "Running DirtBag Pi in the background"
source venv/bin/activate
pip3 install -r requirements.txt
nohup python3 app/app.py &
