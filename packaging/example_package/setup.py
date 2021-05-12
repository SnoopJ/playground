from setuptools import setup, find_packages

setup(
    name="pyntsize",
    description="A smol example project",
    license="MIT",
    classifiers = [
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(
        where="src",
        include=["pyntsize", "_pyntsize"]
    ),
    package_dir={"": "src"},
    install_requires=[
        "pytest"
    ],
)
