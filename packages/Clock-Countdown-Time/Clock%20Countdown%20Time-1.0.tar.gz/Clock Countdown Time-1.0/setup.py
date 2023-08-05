from os import name
from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

setup(
    name="Clock Countdown Time",
    version="1.0",
    description="Used to countdown time",
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url="",
    author="JohanCoder",
    author_email="immrwant@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="countdown",
    packages=find_packages(),
    install_requires=["time"]
)