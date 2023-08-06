import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xmltocd",
    version="0.2.2.1",
    author="jiyang",
    author_email="jiyangj@foxmail.com",
    description="An effective, powerful, fast and simple XML Python parsing tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JIYANG-PLUS/xml-to-chain-dict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)