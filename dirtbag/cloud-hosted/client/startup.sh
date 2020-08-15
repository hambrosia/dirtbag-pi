#! /bin/bash

echo "Running DirtBag Pi in the background"
pip3 install -r requirements.txt
source venv/bin/activate
nohup python3 app/app.py &
