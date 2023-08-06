import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="genpurp",
    version="0.0.1",
    author="Hugo Carvalho",
    author_email="hugodanielsilvacarvalho.hc@gmail.com",
    description="General-purpose library of utilities and extensions to the pandas standard library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hugodscarvalho/genpurp",
    packages=setuptools.find_packages(),
    keywords=['python', 'general purpose', 'pandas', 'complement', 'data'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)