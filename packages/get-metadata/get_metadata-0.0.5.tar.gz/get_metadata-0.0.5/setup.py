import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="get_metadata",
    version="0.0.5",
    author="Hisashi Murai",
    author_email="xyksp956@yahoo.co.jp",
    description="Get metadata string. Works on GAE(Google App Engine), GCF(Google Cloud Functions), and the others.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hisashimurai/get_metadata",
    keywords="GAE GCF GCP metadata",
    packages=["get_metadata"],
    install_requires=[],
    license="MIT",
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
