import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KeiAPI",
    version="1.0.1",
    author="Onkar Dahale",
    author_email="dahaleonkar@gmail.com",
    description="Kei is an unofficial, Pure Python API for gogoanime2.org.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["Kei"],
    package_dir={"": "src"},
    python_requires=">=3.9.5",
    url="https://github.com/onkardahale/kei",
    keywords = ["api", "BeautifulSoup", "gogoanime", "webscraper", "JSON"],
    install_requires=["bs4","requests"],
    project_urls={
        "Bug Tracker": "https://github.com/onkardahale/kei/issues",
    },
    classifiers={
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    },

)
