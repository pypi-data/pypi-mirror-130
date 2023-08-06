from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE/ "README.md").read_text()

setup(
    name="lahg_ad",
    version="1.1.0",
    description="A simple AutoDiff package that supports forward and reverse differentiation, brought to you by the LAHG Society.",
    long_description=README,
    long_description_content_type='text/markdown',
    url="https://https://github.com/cs107-lahg/cs107-FinalProject",
    auther='LAHG Society',
    license='MIT',
    packages=['lahg_ad'],
    install_requires = ["numpy~=1.19"]
)