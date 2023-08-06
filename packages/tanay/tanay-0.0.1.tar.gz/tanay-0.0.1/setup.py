from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'tanay'
LONG_DESCRIPTION = 'A package to detect hands using your webcam'

# Setting up
setup(
    name="tanay",
    version=VERSION,
    author="Tanay Baviskar",
    author_email="tanaybaviskar@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv', 'mediapipe'],
    keywords=['tanay', 'tanay baviskar', 'hand tracking module', 'handtrackingmodule', 'mediapipe', 'python', 'opencv', 'ai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
