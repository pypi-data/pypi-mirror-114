# Import our newly installed setuptools package.


__VERSION__ = "0.1"

import setuptools

# Opens our README.md and assigns it to long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read()

setuptools.setup(
    name="suffuse_log",
    version=__VERSION__,
    description="""
   Log that utilizes ansi-codes to color and stylize log messages. Allows for configurable/conditional styling.
   """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nick Lawrence",
    author_email="ncg-l@outlook.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=requirements,
)
