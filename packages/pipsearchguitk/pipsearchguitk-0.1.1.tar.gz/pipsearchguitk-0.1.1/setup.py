from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(

    name="pipsearchguitk",
    version = "0.1.1",
    author='Ashwin.B',
    license='GPL v3',
    author_email = 'ahnashwin1305@gmail.com',
    url = 'https://github.com/ahn1305/pipsearchguitk',
    description = "Check whether a particular package is available in your system",
    long_description = long_description,
    long_description_content_type= "text/markdown",
    py_modules = ["pipsearchguitk"],
    package_dir = {'':'src'},


    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],

)