from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='helloworld_examplePackage',
    version='0.0.1',
    description='Say hello!',
    py_modules=["helloworld_examplePackage"],
    package_dir = {'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # GNU General Public License v2 or later (GNUv2)
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",

    # For developing or testing `extras_require`
    # Be as version specific as possible, not neccesarily fixed versions
    extras_require = {
        "dev": [
            "pytest>=3.8",
            "twine"
        ],
    },

    url="https://github.com/drewamorbordelon/helloworld-PyPI",
    author="Drew Bordelon",
    author_email="bordelon.drew@gmail.com",

    # If using particular `Library Dependencies` to run module
    # install_requires = [
    #     "blessings ~= 1.7"
    # ],
)