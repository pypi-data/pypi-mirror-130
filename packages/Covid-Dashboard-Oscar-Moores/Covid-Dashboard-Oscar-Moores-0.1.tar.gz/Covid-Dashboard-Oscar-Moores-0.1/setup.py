import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "Covid-Dashboard-Oscar-Moores",
    version = "0.1",
    author = "Oscar Moores",
    author_email = "om368@exeter.ac.uk",
    description = long_description ,
    long_description_content_type = "text/markdown",
    url = "https://github.com/FieldMarshalGaig/Covid-dashboard",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires = ">= 3.10.0",
)