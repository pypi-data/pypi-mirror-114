from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="pybetaface",
    version="1.1",
    description="Use the BetaFace API in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamd47/pybetaface",
    author="WilliamD47",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pybetaface"],
    include_package_data=True,
    install_requires=["requests"],
)