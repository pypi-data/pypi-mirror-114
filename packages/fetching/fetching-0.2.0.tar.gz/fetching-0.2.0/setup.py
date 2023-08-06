from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fetching",
    version="0.2.0",
    packages=find_packages(),
    install_requires=["PyGithub"],
    license="MIT",
    url="https://github.com/nthparty/fetching",
    author="bengetch",
    author_email="bengetch@gmail.com",
    description="Python tool for automatically wrapping multiple (possibly private) Python libraries "
                "into a single portable module file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8"
)
