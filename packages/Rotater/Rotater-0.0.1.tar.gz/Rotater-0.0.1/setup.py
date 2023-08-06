from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'lakshay'
LONG_DESCRIPTION = 'A package to perform screen rotating operations'

# Setting up
setup(
    name="Rotater",
    version=VERSION,
    author="Lakshay",
    author_email="sharmalakshay0208@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['rotatescreen'],
    keywords=['hacking', 'math', 'mathematics', 'python tutorial', 'Lakshay Sharma'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)