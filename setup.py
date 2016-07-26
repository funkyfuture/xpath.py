from setuptools import setup, find_packages
import sys


install_requires = []
if sys.version_info < (3, 4):
    install_requires.append("enum34")


setup(
    name="xpath",
    version="0.0.1",
    description="Python library for generating XPath expressions",
    long_description="Python library for generating XPath expressions",
    url="https://github.com/elliterate/xpath.py",
    author="Ian Lesperance",
    author_email="ian@elliterate.com",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=install_requires,
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "selenium"])
