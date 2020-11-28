#!/usr/bin/env bash
pip install -r requirements.txt
flask db upgrade
flask run -h 0.0.0.0
