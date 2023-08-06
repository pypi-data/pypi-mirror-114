from os import name
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scanfs",
    version="0.0.6",
    description="File system scanner in Python",
    author="CPU Info",
    author_email="cpuinfo10@gmail.com",
    extra_requires=dict(tests=["pytest"]),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url="https://github.com/cpuinfo/scanfs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
