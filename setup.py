#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip._internal.req import parse_requirements
from setuptools import setup

import pdf_preflight


version = pdf_preflight.__version__

readme = open('README.md').read()

requirements = [req.requirement for req in parse_requirements('requirements.txt', session=False)]

setup(
    name='pdf-preflight',
    version=version,
    description="""Check if PDF files are standards compliant""",
    long_description=readme,
    author='Draft2Digital',
    author_email='jennifer.easter@draft2digital.com',
    url='https://github.com/Draft2Digital/pdf-preflight',
    packages=[
        'pdf_preflight',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='pdf-preflight',
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

