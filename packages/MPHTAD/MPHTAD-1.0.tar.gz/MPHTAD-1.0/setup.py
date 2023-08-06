from setuptools import setup, find_packages

setup(
    name="MPHTAD",
    version="1.0",
    author="Harvard CS107 Final Project Group MPHTAD",
    description="A package for automatic differentiation",
    url="https://github.com/cs107-MPHT/cs107-FinalProject.git",
    tests_require=["pytest"],
    packages=['MPHTAD'],
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)