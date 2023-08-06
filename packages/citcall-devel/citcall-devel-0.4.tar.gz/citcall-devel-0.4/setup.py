import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="citcall-devel",
    version="0.4",
    author="Citcall",
    author_email="devel@citcall.com",
    description="Citcall REST API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/citcall/citcall-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)