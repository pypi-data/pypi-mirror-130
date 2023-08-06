import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Covid-Dashboard-pkg-tsturgeon",
    version="0.0.1",
    author="Tom Sturgeon",
    author_email="ts709@exeter.ac.uk",
    description="A Covid Dashboard to show current news and data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sturgeon2962/coursework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.7',
)
