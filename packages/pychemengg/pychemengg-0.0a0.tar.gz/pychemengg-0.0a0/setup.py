import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pychemengg", 
    version="0.0a0",
    author="Prof. Harvinder Singh Gill",
    author_email="harvinder.gill@ttu.edu",
    description="A python package to facilitate teaching of chemical engineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/profhsgill",
    keywords=["chemical engineering", "chemical-engineering", 
              "heat transfer","heat-transfer", 
              "material balances","material-balances",
              "chemical reaction engineering",
              "thermodynamics", "reactions",
              "reactors", "reaction-engineering",
              "process control", "fluid flow"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",],
    install_requires=["matplotlib", "numpy", "scipy"],
    python_requires='>=3',
)