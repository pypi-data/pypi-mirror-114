from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.13'
DESCRIPTION = 'Streaming video data via networks'
LONG_DESCRIPTION = 'No Documentation now. Just a example for it on github https://github.com/Psyro770/KeyLabs-Python/blob/main/main.py'

setup(
    name="KeyLabsy",
    version=VERSION,
    author="Psyro",
    author_email="<mail@psyro.de>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'pycryptodome'],
    keywords=['wrapper', 'apiwrapper', 'keylabs', 'auth', 'authsystem'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)