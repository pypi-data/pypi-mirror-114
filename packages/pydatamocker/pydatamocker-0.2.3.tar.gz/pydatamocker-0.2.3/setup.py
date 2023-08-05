import setuptools

with open("README.md", "rt", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydatamocker",
    version="0.2.3",
    author="Maxim Soukharev",
    author_email="maxim.soukharev@gmail.com",
    description="A data mocker for python scripts and jupyter notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msoukharev/pydatamocker",
    project_urls={
        "Bug Tracker": "https://github.com/msoukharev/pydatamocker",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where='.'),
    python_requires=">=3.7",
)
