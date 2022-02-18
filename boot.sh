#!/bin/bash
source venv/bin/activate
flask db upgrate
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app