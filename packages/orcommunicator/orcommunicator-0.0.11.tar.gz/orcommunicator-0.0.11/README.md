This module is responsible for mananing communication of the different microservices of the OpenResearch API.

## Create Package

pip3 install setuptools twine 
python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*

pip install YOURPACKAGE --upgrade