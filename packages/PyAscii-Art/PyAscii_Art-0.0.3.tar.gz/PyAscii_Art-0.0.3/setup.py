import setuptools
from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="PyAscii_Art",
    version="0.0.3",
    description="Image to ASCII art images library.",
    author="ImGajeed",
    url="https://github.com/ImGajeed76/PyAscii-Art",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=["ascii", "art", "ascii-art", "image", "ascii-image"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
    py_modules=["PyAsciiArt"],
    package_dir={"": "src/pyAsciiArt"},
    install_requires=[
        "Pillow"
    ]
)