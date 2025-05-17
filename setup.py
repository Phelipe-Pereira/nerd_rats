from setuptools import setup, find_packages

setup(
    name="nerd_rats",
    version="0.1",
    packages=find_packages(),
    install_requires=["pynput>=1.7.6", "requests>=2.31.0", "python-dotenv>=1.0.0"],
)
