import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indicators_py",
    version="0.0.1",
    author="Amir Talic",
    description="Package of different trading indicators for use on crypto bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["indicators_py"],
    package_dir={'':'indicators_py/src'},
    install_requires=[]
)