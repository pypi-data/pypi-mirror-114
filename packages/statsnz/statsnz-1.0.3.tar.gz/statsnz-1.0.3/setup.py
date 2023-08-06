
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="statsnz",
    version="1.0.3",
    description="A collection of functions to enable ease of use of the various Stats NZ APIs",
    long_description=README,
    long_description_content_type="",
    url="https://github.com/basanovase/statsnz",
    author="Flynn",
    author_email="flynn.mclean@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["statsnz"],
    include_package_data=True,
    install_requires=["pandas", "requests"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
