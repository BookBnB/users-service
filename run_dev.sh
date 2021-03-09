#!/usr/bin/env bash
PATH=$PATH:$HOME/.local/bin
export FLASK_DEBUG=1
pip install -r requirements.txt --user
flask db upgrade
flask run -h 0.0.0.0
