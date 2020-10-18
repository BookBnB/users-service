#!/usr/bin/env bash
flask db upgrade
waitress-serve --port $PORT --call 'project:create_app'
