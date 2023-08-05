import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orcommunicator",
    version="0.0.11",
    author="Leonardo de Araújo",
    author_email="dearaujo@uni-bremen.de",
    description="OpenResearch microservices communication management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonardomra/orcommunicator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ["boto3==1.14.25", "Flask>=1.0.4", "ordbhandler>=0.0.1"],
)