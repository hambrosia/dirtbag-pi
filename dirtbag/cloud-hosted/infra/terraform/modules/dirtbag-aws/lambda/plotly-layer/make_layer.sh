#!/bin/bash

mkdir -p python
pip3 install -r requirements.txt -t python
zip -r plotly_layer.zip ./python