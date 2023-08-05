import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sciformlib",
    version="1.0.0_dev_1",
    description="A Simplified Science Formula Library, to solve science problems with few more easy steps.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="iamrealbhuvi",
    author_email="bhuvanesh19112001@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["sciformlib"],
    include_package_data=True,
    install_requires=["numpy"],
    entry_points={
        "console_scripts": [
            "square=square.__main__:main",
        ]
    },
)
