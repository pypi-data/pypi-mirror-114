"""tochsdk setup.py
"""
from setuptools import setup, find_packages

setup(
    name="tochsdk",
    version="0.1.0",
    description="Toch ai commond line interface",
    packages=find_packages(),
    install_requires=[
        "fire"
    ],
    entry_points={
        'console_scripts': ['tochcli=tochsdk.tochsdk:main']
    },
    author="toch team",
    license="MIT"
)
