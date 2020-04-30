#!/bin/bash

mkdir -p python
pip3 install -r requirements.txt -t python
zip -r plot_layer.zip ./python