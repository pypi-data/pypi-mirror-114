This module is responsible for mananing communication of the OpenResearch API with AWS S3.

## Create Package

pip3 install setuptools twine 
python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*

pip install YOURPACKAGE --upgrade