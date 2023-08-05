from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="avocentpdulib",
    python_requires=">3.5.2",
    version="0.0.1",
    author="Howaner",
    author_email="me@reiterfranz.de",
    description="Feature-rich methods to control avocent pdu's in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Howaner/avocentpdulib",
    download_url="https://github.com/Howaner/avocentpdulib/archive/refs/tags/v0.0.1.tar.gz",
    packages=find_packages(),
    install_requires=[
        "defusedxml",
        "urllib3",
        "aiohttp"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
