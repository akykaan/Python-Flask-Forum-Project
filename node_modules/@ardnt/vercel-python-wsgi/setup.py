#! /usr/bin/env python
import json

from setuptools import setup


with open('package.json') as f:
    package_data = json.loads(f.read())
    version = package_data['version']


"""A barebones setup for tests
"""
setup(
    name='vercel-python-wsgi',
    version=version,
    packages=[
        'vercel_python_wsgi'
    ],
    install_requires=[
        'Werkzeug==1.0.1',
    ]
)
