#setup.py

from setuptools import _install_setup_requires, setup
with open('requirements.txt') as f:
    requirements = f.readlines()
setup(
    name='gitci',
    version='0.0.1',
    install_requires = ["PyGithub==1.55","click==8.0.1"],
    entry_points={
        'console_scripts': [
            'gitci =gitci:gitci'
        ]
    }
)