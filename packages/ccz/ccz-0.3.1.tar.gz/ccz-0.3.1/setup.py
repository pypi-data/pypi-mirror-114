from setuptools import setup, find_packages

setup(
    name="ccz",
    version="0.3.1",
    install_requires=["ccxt"],
    packages=find_packages(),
    entry_points={"console_scripts": ["ccz=ccz:main"]},
    python_requires=">=3.6",
)
