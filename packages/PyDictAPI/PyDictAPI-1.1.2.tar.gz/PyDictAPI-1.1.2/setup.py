from setuptools import setuptools, find_packages

classifiers = [
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ]

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="PyDictAPI",
    version="1.1.2",
    author="Shawan Mandal",
    author_email="imshawan.dev049@gmail.com",
    description="A simple web-scraping based Dictionary Module for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imshawan/PyDictAPI",
    packages=find_packages(),
    classifiers=classifiers,
    install_requires=[
        'bs4',
        'requests'
    ]
)