import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ez-pg",                     # This is the name of the package
    version="1.1.3",                        # The initial release version
    author="Adam Weaver",                     # Full name of the author
    description="Query Builder to simplify working in postgres databases using Psycopg2",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages('psycopg2'),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["ez_pg"],             # Name of the python package
    package_dir={'':'ez_pg/src'},     # Directory of the source code of the package
    install_requires=['psycopg2']                     # Install other dependencies if any
)