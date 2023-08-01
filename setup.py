import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="omae-common-lib-pkg",
    version="0.0.152",
    author="JusticePayments",
    author_email="just-admin@justpayments.co.kr",
    description="JusticePayments common lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Just-Payments/OmaeCommon",
    project_urls={
        "Bug Tracker": "https://github.com/Just-Payments/OmaeCommon/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires = [
        'Django'
    ],
    license='MIT',
)