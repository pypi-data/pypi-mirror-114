import setuptools
from pathlib import Path

setuptools.setup(
  name="reverseit",
  version='1.0.4',
  long_description=Path("README.md").read_text(),
  packages=setuptools.find_packages(exclude=["tests", "data"])
)