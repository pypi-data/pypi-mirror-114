import setuptools
from pathlib import Path

setuptools.setup(
    name="pdfpackage_17",
    version="1.0.3",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
