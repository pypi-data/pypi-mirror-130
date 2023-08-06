# -*- coding: ascii -*-
"""
package/install mailutil
"""

import sys
import os
from setuptools import setup

PYPI_NAME = 'mailutil'

sys.path.insert(0, os.getcwd())

import mailutil

setup(
    #-- Package description
    name=PYPI_NAME,
    license='Apache License, Version 2.0',
    version=mailutil.__version__,
    description='mail utility module',
    long_description="""mailutil:
This module contains
1. wrapper classes for smtplib.SMTP for better TLS support
2. Factory function which opens SMTP connections described by URL
""",
    author='Michael Stroeder',
    author_email='michael@stroeder.com',
    maintainer='Michael Stroeder',
    maintainer_email='michael@stroeder.com',
    url='https://code.stroeder.com/pymod/python-%s' % (PYPI_NAME),
    download_url='https://pypi.python.org/pypi/%s' % (PYPI_NAME),
    project_urls={
        'Code': 'https://code.stroeder.com/pymod/python-%s' % (PYPI_NAME),
        'Issue tracker': 'https://code.stroeder.com/pymod/python-%s/issues' % (PYPI_NAME),
    },
    py_modules=[PYPI_NAME],
    keywords=['SMTP','STARTTLS'],
    python_requires='>=3.6',
)
