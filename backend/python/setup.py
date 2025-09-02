"""
Setup configuration for Psycho-Noir Kontrapunkt backend
"""

from setuptools import setup, find_packages

setup(
    name="psychonoir-kontrapunkt-backend",
    version="0.1.0",
    description="Backend modules for Psycho-Noir Kontrapunkt concept framework",
    author="poisontr33s",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "flask>=2.0.1",
        "flask-cors>=3.0.10",
        "numpy>=1.23.5",
        "pandas>=1.5.3",
        "torch>=2.0.1",
        "scipy>=1.10.1",
        "transformers>=4.30.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)