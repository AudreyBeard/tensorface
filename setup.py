from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tensorface',
    version='0.0.1',
    description='Tensorboard interFace',
    long_description=long_description,
    author='Audrey Beard',
    author_email='audrey.s.beard@gmail.com',
    packages=find_packages(),
    install_requires=[
        'tensorboard>=2.0.0',
    ],
    url='https://gitlab.com/AudreyBeard/tensorface',
        changelog={
            '0.0.0': 'first draft, supports grabbing all scalar values for a given run and for all runs',
            '0.0.1': 'added support to group by scalar names, renamed methods to be more appropriate',
    }
)
