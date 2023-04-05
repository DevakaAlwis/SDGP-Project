#!/bin/bash
# exit or error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
pip install python-dotenv