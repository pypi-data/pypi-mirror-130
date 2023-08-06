from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Vencode API SDK wrapper for Python'
LONG_DESCRIPTION = 'Vencode API SDK wrapper for Python'

setup(
    name="vencode_sdk",
    version=VERSION,
    author="Vencode",
    author_email="hello@vencode.io",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'video encoding', 'transcoding'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)