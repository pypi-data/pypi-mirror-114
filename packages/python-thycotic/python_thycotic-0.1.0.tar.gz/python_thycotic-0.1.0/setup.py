from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="python_thycotic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.0",
    description="Python wrapper for Thycotic Secret Server API",
    url="https://github.com/ksalman/python_thycotic",
    author="ksalman",
    author_email="1268871+ksalman@users.noreply.github.com",
    license="Apache Software License",
    packages=["thycotic"],
    install_requires=["requests ~=2.25.1"],
    zip_safe=False,
)
