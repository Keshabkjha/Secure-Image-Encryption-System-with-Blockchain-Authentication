"""
Setup script for Secure Image Encryption System.

This script handles the package installation and metadata.
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

def read_requirements(file_path: str) -> list:
    """Read requirements from a file.
    
    Args:
        file_path: Path to the requirements file
        
    Returns:
        List of requirements
    """
    requirements = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                # Remove any trailing comments
                requirement = line.split('#', 1)[0].strip()
                if requirement:
                    requirements.append(requirement)
    return requirements

# Directory containing this file
HERE = Path(__file__).parent

# The text of the README file
with open(HERE / 'README.md', 'r', encoding='utf-8') as f:
    README = f.read()

# Get the version from the package
version = {}
with open(HERE / 'secure_image_encryption' / '__init__.py', 'r', encoding='utf-8') as f:
    exec(f.read(), version)

# Get requirements
install_requires = read_requirements('requirements.txt')

# Development requirements
extras_require = {
    'dev': read_requirements('requirements-dev.txt'),
}

# This call to setup() does all the work
setup(
    name="secure-image-encryption",
    version=version.get('__version__', '0.1.0'),
    description="Secure Image Encryption System with Blockchain Authentication",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/secure-image-encryption",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=['secure_image_encryption', 'secure_image_encryption.*']),
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'secure-image=secure_image_encryption.__main__:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/secure-image-encryption/issues',
        'Source': 'https://github.com/yourusername/secure-image-encryption',
    },
)
