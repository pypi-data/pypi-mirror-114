import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pubtrend",
    version="0.0.0",
    author="Matt Rybin",
    author_email="mxr2011@miami.edu",
    description="Exploring topic trends using biomedical grants and publications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rybinmj/pubtrend",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
