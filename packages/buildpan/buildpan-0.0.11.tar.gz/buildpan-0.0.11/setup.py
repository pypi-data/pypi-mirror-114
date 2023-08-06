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
from setuptools import _install_setup_requires, setup


setup(
    name='buildpan',
    version='0.0.11',
    packages=["buildpan"],
    install_requires=["click==8.0.1","GitPython==3.1.20","PyGithub==1.52","pyramid==2.0",
"pyramid-resource==0.4.1"],
    entry_points={
        'console_scripts': [
            'buildpan=buildpan.buildpan:buildpan'
        ]
    }
)