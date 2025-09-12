from setuptools import setup, find_packages

setup(
    name="research_tools",
    version="0.3.5",
    packages=find_packages(exclude=['dump_data']),
    install_requires=open("requirements.txt").readlines(),
)
