import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="sniplink",
    version="1.0.0",
    description="API wrapper for the SnipLink API provided by SnipLink.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/billyeatcookies/sniplink-py",
    author="billyeatcookies",
    author_email="billydevbusiness@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    packages=["sniplink"],
    include_package_data=True,
    install_requires=[
        "requests"
    ],
    keywords='api wrapper python3 python sniplink sniplink.py sniplink-py'
)