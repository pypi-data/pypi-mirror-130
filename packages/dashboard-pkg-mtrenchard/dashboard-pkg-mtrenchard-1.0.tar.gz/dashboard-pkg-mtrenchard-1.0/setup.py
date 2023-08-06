import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()

setuptools.setup(
    name="dashboard-pkg-mtrenchard",
    version="1.0",
    author="Matt Trenchard",
    author_email="mjt235@exeter.ac.uk",
    description="A covid dashboard providing the latest Covid information. To be used for demonstration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m4ttT10/2021-Covid-Dashboard-CA",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
