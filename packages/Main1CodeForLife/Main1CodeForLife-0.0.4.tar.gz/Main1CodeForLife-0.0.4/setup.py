from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'yuvraj ka module aka codeforlife'
LONG_DESCRIPTION = 'A package to perform arithmetic operations'

# Setting up
setup(
    name="Main1CodeForLife",
    version=VERSION,
    author="Yuvraj",
    author_email="yuvrajjha24910.dpskalyanpur@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'math', 'mathematics', 'python tutorial', 'yuvraj'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)