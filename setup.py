#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
소리새 AI (Sorisay AI) - 설치 스크립트
Setup script for Sorisay AI System
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
def read_file(filename):
    """Read file contents"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt"""
    requirements = []
    filepath = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

setup(
    name='sorisay-ai',
    version='1.0.0',
    description='소리새 AI - 진화형 AI 어시스턴트 시스템',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='박철홍 (Park Cheol Hong)',
    author_email='parkcheolhong@example.com',
    url='https://github.com/parkcheolhong/run_all_shinsegye.py',
    license='MIT',
    
    # Package discovery
    packages=find_packages(exclude=['tests', 'tests.*', 'example_scripts', 'backup']),
    
    # Include package data
    include_package_data=True,
    package_data={
        '': ['*.json', '*.txt', '*.md'],
    },
    
    # Dependencies
    install_requires=read_requirements(),
    
    # Python version requirement
    python_requires='>=3.8',
    
    # Entry points for command-line scripts
    entry_points={
        'console_scripts': [
            'sorisay=run_all_shinsegye:main',
        ],
    },
    
    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Natural Language :: Korean',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
    # Keywords
    keywords='ai assistant voice-recognition nlp korean music dream-interpretation',
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/parkcheolhong/run_all_shinsegye.py/issues',
        'Source': 'https://github.com/parkcheolhong/run_all_shinsegye.py',
        'Documentation': 'https://github.com/parkcheolhong/run_all_shinsegye.py/blob/main/README.md',
    },
)
