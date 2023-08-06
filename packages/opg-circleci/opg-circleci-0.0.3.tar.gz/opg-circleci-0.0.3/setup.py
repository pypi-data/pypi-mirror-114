import setuptools

with open("shared_code.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opg-circleci",
    version="0.0.3",
    author="OPG",
    author_email="opg-integrations@digital.justice.gov.uk",
    description="Shared Integrations Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ministryofjustice/opg-data",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
