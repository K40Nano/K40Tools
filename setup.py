import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="k40tools",
    version="0.0.1",
    install_requires=[
        "k40nano",
        "pynput"
    ],
    author="Tatarize",
    author_email="tatarize@gmail.com",
    description="K40 Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/K40Nano/K40Tools",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ),
)