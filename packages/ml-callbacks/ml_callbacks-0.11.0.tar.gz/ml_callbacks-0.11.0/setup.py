import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

NAME = "ml_callbacks"
VERSION = "0.11.0"

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

REQUIRES = [
  "ml-tracking-api >= 1.2.5",
  "nbconvert"
]

setup(
    name=NAME,
    version=VERSION,
    description="Simple ml callbacks to track model performance and state",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Eimantas Noreika",
    author_email="noreika.eimantas@gmail.com",
    url="https://github.com/EimantasN/Equusight_BackEnd",
    keywords=["ML", "PyTorch", "Tensorflow", "AI"],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True
)