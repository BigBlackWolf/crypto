#!/bin/bash

virtualenv venv
source venv/bin/activte
pip install -r requirements.txt
psql -U postgres postgres -f ./init.sql
python run.py db init
python run.py db migrate
python run.py db upgrade