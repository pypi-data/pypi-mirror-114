import setuptools
from pathlib import Path
setuptools.setup(
    name="favaspdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # to exclude test and data whic does not contain source code
    packages=setuptools.find_packages(exclude=["unit_test", "sample_data"])
)
