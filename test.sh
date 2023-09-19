#!/usr/bin/bash

# Does the job for now.
# Should not be run unless user ducmagic is setup.

cd /home/ducmagic/

git clone https://github.com/WillemJan/ducmagic/
virtualenv venv

source venv/bin/activate
duc index .

cd ducmagic
pip install .

cd ..
ducmagic index .
ducmagic ls
