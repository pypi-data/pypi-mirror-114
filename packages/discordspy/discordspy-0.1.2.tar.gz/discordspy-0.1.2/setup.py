from setuptools import setup

with open("README.md", "r") as file: description = file.read()

setup(
    name="discordspy",
    version="0.1.2",
    description="A basic API wrapper for Discords.com",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/judev1/discords",
    author="Jude BC",
    author_email="jude.version1.0@gmail.com",
    license="MIT",
    packages=["discordspy"],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
