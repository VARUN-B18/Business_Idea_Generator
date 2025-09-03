#!/usr/bin/env python3
"""
Setup script for Business Idea Creator project
Complete package configuration
"""

from setuptools import setup, find_packages
import os

def read_requirements():
    """Read requirements from requirements.txt"""
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return [
            'streamlit>=1.28.0',
            'openai>=1.3.0', 
            'pandas>=1.5.0',
            'plotly>=5.11.0',
            'requests>=2.28.0',
            'python-dotenv>=0.19.0'
        ]

setup(
    name="business-idea-creator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered business idea generator using advanced prompt engineering",
    long_description="A complete Streamlit application that generates innovative business ideas using OpenAI GPT and advanced prompt engineering techniques.",
    url="https://github.com/your-username/business-idea-creator",
    
    # Package configuration
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    
    # Dependencies
    install_requires=read_requirements(),
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Entry points
    entry_points={
        'console_scripts': [
            'business-idea-creator=business_idea_creator.app:main',
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)