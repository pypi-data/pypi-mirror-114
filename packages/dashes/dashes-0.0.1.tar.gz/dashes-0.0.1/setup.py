from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "-"
LONG_DESCRIPTION = '-'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="dashes",
    version=VERSION,
    author="Arohan Arora",
    author_email="novakcoolguy@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["streamlit"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'dashes package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)