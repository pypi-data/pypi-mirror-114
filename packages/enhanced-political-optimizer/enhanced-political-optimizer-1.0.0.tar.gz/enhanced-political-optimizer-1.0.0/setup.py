import pathlib
from setuptools import setup
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="enhanced-political-optimizer",
    version="1.0.0",
    description="Solve global optimization problems.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/enhanced-political-optimizer",
    author="Danial Saleem",
    author_email="danialsaleem2010@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["numpy", "keras"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
