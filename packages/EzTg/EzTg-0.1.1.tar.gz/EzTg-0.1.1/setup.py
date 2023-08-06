import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EzTg",
    version="0.1.1",
    author="Hexye",
    author_email="dragonsale22@gmail.com",
    description="An api wrapper for telegram easy to use based on telegram core methods.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HexyeDEV/EzTg/",
    download_url="https://github.com/HexyeDEV/EzTg/releases",
    project_urls={
        "Bug Tracker": "https://github.com/HexyeDEV/EzTg/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=["EzTg"],
    python_requires=">=3.6",
    install_requires=['requests>=2.26.0'],
)
