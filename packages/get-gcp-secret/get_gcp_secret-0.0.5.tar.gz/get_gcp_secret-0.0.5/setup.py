import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="get_gcp_secret",
    version="0.0.5",
    author="Hisashi Murai",
    author_email="xyksp956@yahoo.co.jp",
    description="Get value from Google Cloud Secret Manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hisashimurai/get_gcp_secret",
    keywords="GAE GCF GCP secret-manager",
    packages=["get_gcp_secret"],
    install_requires=["google-cloud-secret-manager"],
    license="MIT",
    # https://pypi.org/classifiers/
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
