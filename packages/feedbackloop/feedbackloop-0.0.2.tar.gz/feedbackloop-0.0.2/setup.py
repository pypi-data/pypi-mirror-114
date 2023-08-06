from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'feedback loop greengrass ML component'
LONG_DESCRIPTION = 'a package that allows greengrass devicdes to upload ML inference data to the cloud'

# Setting up
setup(
    name="feedbackloop",
    version=VERSION,
    author="William Xi",
    author_email="williaxi@amazon.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['boto3', 'awsiotsdk'],
    keywords=['python', 'iot', 'aws', 'machine learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)