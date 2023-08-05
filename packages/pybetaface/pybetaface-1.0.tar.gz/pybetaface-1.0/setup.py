from setuptools import setup
setup(
    name="pybetaface",
    version="1.0",
    description="Use the BetaFace API in Python",
    long_description="Use the BetaFace API in Python. Example usage in README",
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