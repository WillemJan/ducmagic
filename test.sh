#!/usr/bin/bash

# Does the job for now.
# Should not be run unless user ducmagic is setup.

# useradd -m ducmagic -s /bin/bash
# rm -rf .duc* ; rm -rf ducmagic/ ; rm -rf venv/; rm -rf out.log ;
# (time bash -x test.sh) > out.log 2>&1

cd /home/ducmagic/

git clone https://github.com/WillemJan/ducmagic/
virtualenv venv

source venv/bin/activate

cd ducmagic
pip install .

cd ..
duc index .
ducmagic index .
ducmagic ls
python ducmagic/ducmagic/ducmagic.py

