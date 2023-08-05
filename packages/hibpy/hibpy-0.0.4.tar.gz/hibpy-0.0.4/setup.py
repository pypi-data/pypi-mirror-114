import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hibpy",
    version="0.0.4",
    author="Geographs",
    author_email="87452561+Geographs@users.noreply.github.com",
    description="Python CLI application to check if you have been pwned.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Geographs/HIBP",
    project_urls={
        "Bug Tracker": "https://github.com/Geographs/HIBP/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
