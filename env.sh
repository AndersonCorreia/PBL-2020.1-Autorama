#!/bin/bash
source ../../Flask/environments/my_env/bin/activate
FLASK_ENV=development
FLASK_APP=app
flask run