from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.3'
DESCRIPTION = 'Fetch market data for the NSE Exchange'
LONG_DESCRIPTION = 'Through the yahoo finance api, we can easily fetch this data'

# Setting up
setup(
    name="data_lelo",
    version=VERSION,
    author="Abhishek Mittal",
    author_email="abhishekmittal964@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests','python-dotenv','datetime','os'],
    keywords=['python','finance','NSE','data','market','trading','investing'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)