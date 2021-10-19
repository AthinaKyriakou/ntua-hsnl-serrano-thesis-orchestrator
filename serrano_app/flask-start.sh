#!/bin/bash

export FLASK_APP=flask_app
cd ./src

# local:
flask run

# prod:
#flask run --host=147.102.16.113
