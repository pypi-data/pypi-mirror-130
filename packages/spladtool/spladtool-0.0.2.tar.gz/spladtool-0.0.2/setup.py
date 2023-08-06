import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name = "spladtool",
    version = "0.0.2",
    author = "Raymond Jow, Rye Julson, Shihan Lin, Yuanbiao Wang",
    author_email = "rjow@college.harvard.edu",
    description = "The Simple Pytorch-Like Auto Differentiation Toolkit is an automatic differentiation package for calculating gradients of a function in forward and reverse mode.",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/cs107-rysr/cs107-FinalProject",
    license = "MIT",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires = ">=3.7",
    install_requires = ["numpy"],
)
