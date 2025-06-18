#!/usr/bin/env python3
"""
SYLVA Setup Script
Simple setup configuration for the Symbolic Emotional Wellness Assistant
"""

from setuptools import setup, find_packages

setup(
    name="sylva",
    version="2.0.0",
    description="Symbolic Emotional Wellness Assistant - A trauma-safe, metaphor-driven CLI",
    author="Forest Within Therapeutic Services Professional Corporation",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pathlib2>=2.3.7",
    ],
    entry_points={
        "console_scripts": [
            "sylva=main:app",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Utilities",
    ],
)
