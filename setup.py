import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lnt",
    version="0.0.1",
    author="Harsha Goli",
    author_email="harshagoli@gmail.com",
    description="A better lncli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/lnt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
