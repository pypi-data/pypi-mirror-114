from os import path
from setuptools import setup
from pyhapwol import __version__

root = path.abspath(path.dirname(__file__))
with open(path.join(root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyhapwol',
    version=__version__,
    description="A Wake on LAN Switch implementation for HomeKit",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/aquator/hap-wol-python',
    author="István Rábel",
    author_email="thraex.aquator@icloud.com",
    license="Unlicense",
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["pyhapwol"],
    python_requires=">=3.6",
    install_requires=[
        "click~=8.0.0",
        "hap-python~=3.5.0",
        "pywol~=1.0.0",
        "pyyaml~=5.4.0",
        "scapy~=2.4.0"
    ],
    entry_points="""
        [console_scripts]
        pyhapwol=pyhapwol.cli:run
    """
)
