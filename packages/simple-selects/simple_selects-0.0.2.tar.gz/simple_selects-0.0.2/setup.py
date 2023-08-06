from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Simple_selects'
LONG_DESCRIPTION = 'Simple, but not very'

setup(
    name="simple_selects",
    version=VERSION,
    author="Violetta Kishkurno",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pypika'],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: Microsoft :: Windows",
    ]
)
