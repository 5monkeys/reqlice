#!/usr/bin/env python
from os import path
from pkg_resources import parse_requirements
from setuptools import setup, find_packages

name = 'reqlice'  # PyPI name
here = path.dirname(path.abspath(__file__))

# Get the long description from the relevant file
long_description = None

try:
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    pass


def get_requirements(filename):
    return [str(r) for r in parse_requirements(open(filename).read())]


setup(
    name=name,
    version='1.0.0',
    url='https://github.com/5monkeys/reqlice',
    license='MIT',
    author='Akseli Nelander',
    author_email='akseli@5monkeys.se',
    description='Fetches and annotates the license of pip requirements.',
    long_description=long_description,
    packages=find_packages(include='reqlice'),
    entry_points={
        'console_scripts': [
            'reqlice = reqlice:cli'
        ]
    },
    install_requires=get_requirements('requirements.txt'),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ]
)
