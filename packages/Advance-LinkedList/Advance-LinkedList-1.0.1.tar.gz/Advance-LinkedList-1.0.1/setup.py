import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.MD").read_text()

# This call to setup() does all the work
setup(
    name="Advance-LinkedList",
    version="1.0.1",
    description="It is LinkedList Data Structure",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nit22032002/Advance-LinkedList",
    author="Nitin",
    author_email="nit2203@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["linkedlist"],
    include_package_data=True,
    install_requires=[],
)