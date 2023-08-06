import setuptools


setuptools.setup(
    name="easyensembling",                     # This is the name of the package
    version="0.0.3",                        # The initial release version
    author="dv",                     # Full name of the author
    packages=setuptools.find_packages(),    # List of all python modules to be installed                                     # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["easyensembling"],             # Name of the python package
    package_dir={'': 'easyensembling/'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)