#setup.py

from setuptools import _install_setup_requires, setup
# with open('requirements.txt') as f:
#     requirements = f.readlines()
setup(
    name='buildpan',
    version='0.0.12',
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
    entry_points={
        'console_scripts': [
            # 'gitci =gitci:gitci'
            'buildpan=buildpan.buildpan:buildpan'
        ]
    }
)