#!/usr/bin/bash

# Does the job for now.
# Should not be run unless user ducmagic is setup.

cd /home/ducmagic/

rm -rf ducmagic/
rm -rf venv/
rm -rf .duc*

git clone https://github.com/WillemJan/ducmagic/
virtualenv venv

source venv/bin/activate
duc index .

cd ducmagic
pip install .

cd ..
ducmagic index .
ducmagic ls

source venv/bin/deactivate
