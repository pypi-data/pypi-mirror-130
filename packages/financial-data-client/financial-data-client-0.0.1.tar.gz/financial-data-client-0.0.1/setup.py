import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="financial-data-client",
    version="0.0.1",
    author="Max Leonard",
    author_email="maxhleonard@gmail.com",
    description="Package for easily retrieving price data from multiple sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxhleonard/financial-data-client",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src","FinData":"src/FinData"},
    packages=["FinData"],
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "python-binance",
        "kucoin-python"
    ]
)