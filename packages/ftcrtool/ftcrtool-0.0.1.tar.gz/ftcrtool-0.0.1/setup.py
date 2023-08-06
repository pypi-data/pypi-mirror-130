import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ftcrtool",
    version="0.0.1",
    author="terrytan",
    author_email="terrytan@futunn.com",
    description="post or update Code Review",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.futunn.com/terrytan/ftcrtool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
