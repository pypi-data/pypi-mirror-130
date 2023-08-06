import setuptools
import subprocess
import os

publish_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

setuptools.setup(
    name="random-functions",
    version=publish_version,
    author="Bipin",
    author_email="test@test.com",
    license="MIT",
    description="Test library",
    long_description="test library",
    long_description_content_type="text/markdown",
    url="https://github.com/bipinkrishnan/test-library",
    packages=setuptools.find_packages(),
    keywords=['test'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "requests >= 2.25.1",
    ],
)
