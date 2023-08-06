
from setuptools import setup, find_packages
  
long_description = """
initiate the cli with "buildpan" 
 Use "buildpan auth" for authentication \n 
 Use "buildpan allrepo" for displaying all the repositories \n 
 Use "buildpan selectrepo" for selecting repo \n 
 Use "buildpan crepo" create repo in github 
"""  
setup(
        name ='buildpan',
        version ='0.0.22',
        author ='Akash Dwivedi',
        url ='https://github.com/Vibhu-Agarwal/vibhu4gfg',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'buildpan = buildspan.gitci:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='Akash dwivedi',
            install_requires = ["PyGithub==1.55","click==8.0.1","idna==3.2",
"platformdirs==2.1.0",
"pycparser==2.20",
"PyJWT==2.1.0",
"PyNaCl==1.4.0",
"requests==2.26.0",
"six==1.16.0",
"urllib3==1.26.6",
"virtualenv==20.6.0",
"wrapt==1.12.1",
"backports.entry-points-selectable==1.1.0",
"certifi==2021.5.30",
"cffi==1.14.6",
"charset-normalizer==2.0.3",
"colorama==0.4.4",
"Deprecated==1.2.12",
"distlib==0.3.2",
"filelock==3.0.12"],
        zip_safe = False
)