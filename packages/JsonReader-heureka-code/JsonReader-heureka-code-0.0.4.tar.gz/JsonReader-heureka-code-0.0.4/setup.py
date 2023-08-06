import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="JsonReader-heureka-code",
    version="0.0.4",
    author="heureka-code",
    long_description=long_description,
    license="MIT",
    description="Verarbeitet JSON",
    url="https://github.com/heureka-code/JsonReader-heureka-code",
    download_url="https://github.com/heureka-code/JsonReader-heureka-code/archive/refs/tags/0.0.4.tar.gz",
    packages=setuptools.find_packages()
    )
