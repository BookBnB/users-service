#!/usr/bin/env bash
dotenv run flask db upgrade
dotenv run bash -c 'waitress-serve --port $PORT --call "project:create_app"'
