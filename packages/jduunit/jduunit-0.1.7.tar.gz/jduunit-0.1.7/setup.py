import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="jduunit",
    version="0.1.7",
    scripts=["bin/jduunit"],
    author="Jean Demeusy",
    author_email="dev.jdu@gmail.com",
    description="A simple unittesting package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeandemeusy/jdu_unit",
    packages=["jduunit"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["jduargs"],
)
