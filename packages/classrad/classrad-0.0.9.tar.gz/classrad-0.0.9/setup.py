import setuptools
from setuptools import setup

# Load packages from requirements.txt
with open("requirements-min.txt") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

setup(
    name="classrad",
    packages=setuptools.find_packages(),
    package_data={"classrad.config":
["classrad/config/*"]},
    install_requires=required_packages,
)
