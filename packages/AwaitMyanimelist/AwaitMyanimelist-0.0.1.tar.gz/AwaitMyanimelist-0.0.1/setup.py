from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'a async package for myanimelist api v2'

# Setting up
setup(
    name="AwaitMyanimelist",
    version=VERSION,
    author="resetxd",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['aiohttp'],
    keywords=['python', 'async', 'mal', 'myanimelist', 'api', 'api wrapper','discord'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)