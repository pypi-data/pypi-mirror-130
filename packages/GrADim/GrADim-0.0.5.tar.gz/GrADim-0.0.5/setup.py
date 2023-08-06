from setuptools import setup, find_packages

setup(
    name="GrADim",
    version="0.0.5",
    author=["Aloysius Lim", "Gregoire Baverez", "Shivam Raval", "Xinrong Yang"],
    description="A package for auto-differentiation",
    url="https://github.com/cs107-i-m-i-m/cs107-FinalProject",
    tests_require=["pytest"],
    packages=['GrADim'],
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
