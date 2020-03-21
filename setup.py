# -*- coding: utf-8 -*-
"""
    flask_wangeditor
    ~~~~~~~~~~~~~~~

    :author: Nuctori <Nuctori@foxmail.com>
    :copyright: (c) 2020 by Nuctori.
    :license: MIT, see LICENSE for more details.
"""
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Flask-wangEditor',
    version='0.0.3.1',
    url='https://github.com/Nuctori/flask_wangEditor',
    license='MIT',
    author='Nuctori',
    author_email='Nuctori@foxmail.com',
    description='wangEditor integration for Flask.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['flask_wangEditor'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
