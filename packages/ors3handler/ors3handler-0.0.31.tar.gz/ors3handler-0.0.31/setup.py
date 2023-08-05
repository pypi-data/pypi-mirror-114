import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ors3handler",
    version="0.0.31",
    author="Leonardo de Araújo",
    author_email="dearaujo@uni-bremen.de",
    description="AWS S3 Data Management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leonardomra/s3handler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ["boto3==1.14.25", "botocore==1.17.47", "Werkzeug<1.0.1,>=0.16.1"],
)