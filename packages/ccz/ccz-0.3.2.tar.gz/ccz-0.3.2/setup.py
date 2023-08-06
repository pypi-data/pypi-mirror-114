from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="ccz",
    version="0.3.2",
    install_requires=["ccxt"],
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["ccz=ccz:main"]},
    python_requires=">=3.6",
)
