from setuptools import setup, find_packages

setup(
    name="personal_tools",
    version="0.1",
    packages=find_packages(exclude=['dump_data']),
    install_requires=open("requirements.txt").readlines(),
)