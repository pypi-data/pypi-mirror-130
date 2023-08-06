from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'package to scrape live quotes from yahoofinance using threading'
LONG_DESCRIPTION = "package to use threading to get live quotes of a list of symbols, inspired by stockquotes package"

setup(
    name="yfQuotes",
    version=VERSION,
    author='Justin Law',
    author_email="justin.kklaw@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
    'beautifulsoup4==4.9.3'
    'aiohttp==3.8.1',
    'websocket-client==1.2.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"   
)