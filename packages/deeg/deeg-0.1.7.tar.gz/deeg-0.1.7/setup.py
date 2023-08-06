from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="deeg",
    version="0.1.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.17.0",
        "matplotlib>=3.1.3",
        "scikit-learn>=0.23.2",
    ],
    author="Jiaqi Li, Zhihao Zhao, Yiming Li",
    author_email="lijiaqi199609@sina.com, sethzhao506@berkeley.edu",
    description="package for EEG data analysis and deep learning",
    license="MIT",
    url="https://github.com/pypa/sampleproject",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
