from setuptools import setup
import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="heligeo",
    version = '1.0.4',
    description="Python client for requests to heligeo API services",
    long_description = README,
    long_description_content_type="text/markdown",
    author="Heliware",
    author_email="explore@heliware.co.in",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["heligeo"],
    install_requires=["requests"]
)