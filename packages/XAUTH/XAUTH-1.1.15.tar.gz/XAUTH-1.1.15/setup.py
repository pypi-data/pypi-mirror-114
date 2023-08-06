from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.1.15'
DESCRIPTION = 'Package for xauth.ml'
LONG_DESCRIPTION = 'Not public uses '

setup(
    name="XAUTH",
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