# Python Starter Package
This is a basic python starter package to be used as a template for creating your own python packages.

## Installation
Currently, this library is not hosted on PyPi. Once it is available, you would be able to install via ```pip```:
```
pip install python_starter_package
```
For manual install, see below.

### Manual Install
To manually install this app, clone this repo to your local system. After you clone the repo, navigate into the package to where the ```setup.py``` file is. Then use ```pip install -e .``` command. This will install the package and all its dependencies editable mode. Then you can use the package locally or use it as the starting point for building out your own package.
```
pip install -e .
```

## Usage
You can run this app in your terminal with:
```
./app.py
```

Alternatively, you can import this app in your own project and run it within your program. For example:
```
from python_starter_package import *

python_starter = PythonStarterPackage()
python_starter.run()
```

## Documentation
The purpose of this guide is to show how to create this standard python package from scratch. See packaging.python.org for more details: https://packaging.python.org/tutorials/packaging-projects/. 

### Setup
In order to setup the your own standard python package from scratch do the following:

1. Setup the starter package with the files and folders below:
* config - Directory containing all configuration files for your package.
* src/python_starter_package - Core directory containing all the files that make up your program as well as __init__.py which is the entry point to our package.
 * utils - Directory containing any utility files for your program.
* test - Directory containing all your test scripts.
* app.py - Script to run your application.
* LICENSE - File defining your package's license.
* README.md - Readme file for documentation.
* requirements.txt - File defining all the requirements of your package.
* setup.py - Script to build your package.

2. Once setup, add the contents and code to the files and directories you created. Copy the contents and code from the PythonStarterPackage available in this repo: https://github.com/mystic-repo/PythonStarterPackage.

3. Create (or overwrite) the requirements.txt document with ```pipreqs```. This is an extremely useful tool because it automatically finds all of the relavent versions of dependencies your package relies on and puts them into the ```requirements.txt``` file. If you don't have ```pipreqs```, install it with ```pip install pipreqs```.
```
pipreqs --force --encoding utf-8
```

### Deployment
Next, create the deployment for this package.

1. Upgrade to ```setuptools```, ```wheel```, and ```twine```.
```
pip3 install --upgrade setuptools wheel twine
pip3 install --user --upgrade setuptools wheel twine
```
2. Build the package with ```setup.py```.
```
python3 setup.py sdist bdist_wheel
```
3. Test the install of the package.
```
pip3 install --user ~/Documents/PythonStarterPackage/dist/python_starter_package-0.1.0-py3-none-any.whl
```
4. Run ```app.py``` to make sure the package is working.
```
./app.py
```

Note: To uninstall the package from pip3 use.
```
pip3 uninstall ~/Documents/PythonStarterPackage/dist/python_starter_package-0.1.0-py3-none-any.whl
```

## Support This Project
If you would like to support this project and future projects donate to my Patreon Page. I'm always looking to add more content for individuals like yourself, unfortunately some of the APIs I would require me to pay monthly fees.
