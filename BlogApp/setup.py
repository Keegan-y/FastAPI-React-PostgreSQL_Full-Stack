#!/usr/bin/env python 
# -*- coding: UTF-8 -*- 
import os
from setuptools import setup

setup(
    name='BlogsBackEndPROD',
    version='0.0.1',
    author='Sai Kumar Yava',
    author_email='saikumar.geek@gmail.com',
    description='Frondend and Backend stack using Python FastAPI, including interactive API documentation',
    platforms='any',
    install_requires=[
        'fastapi',
        'uvicorn',
        'gunicorn',
        'pandas',
        'numpy',
        'psycopg2',
        'sqlalchemy',
        'passlib'
        'python-jose',
        'python-multipart',
        'async-exit-stack'
        'async-generator'
    ],
)
