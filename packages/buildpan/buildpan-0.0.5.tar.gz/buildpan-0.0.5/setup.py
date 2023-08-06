#setup.py

"""
    Title: setup.py
    Module Name: setup.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 29-07-2021
    Description:
        ###############################################################
        ## Setup.py file for the package      ## 
         ###############################################################
 """
from setuptools import _install_setup_requires, setup,find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()
setup(
    name='buildpan',
    version='0.0.5',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'buildpan =buildpan:buildpan'
        ]
    }
)