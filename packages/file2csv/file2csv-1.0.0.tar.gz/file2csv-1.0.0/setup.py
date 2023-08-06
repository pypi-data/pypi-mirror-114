from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file2csv",
    version="1.0.0",
    author="KK Santhanam",
    author_email="KK.Santhanam@gmail.com",
    description="Generates a fixed width file using the provided spec (offset provided in the spec file represent the length of each field).Implements a parser that can parse the fixed width file and generate a delimited file, like CSV for example.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KKSanthanam/file2csv",
    project_urls={
        "Bug Tracker": "https://github.com/KKSanthanam/file2csv/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['wheel'],
    packages=find_packages(exclude=['tests*']),
    python_requires=">=3.9",
)
