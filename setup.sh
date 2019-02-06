#!/bin/bash

virtualenv venv
source venv/bin/activte
pip install -r requirements.txt
psql -U postgres postgres -f ./init.sql
python manage.py makemigrations
python manage.py migrate