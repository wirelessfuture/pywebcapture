import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywebcapture",
    version="0.0.2",
    author="Christopher Andrews",
    author_email="wirelessfuture2000@gmail.com",
    description="A package that allows users to capture full-page screenshots of websites using Selenium and Chrome webdriver.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wirelessfuture/pywebcapture",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freeware",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)