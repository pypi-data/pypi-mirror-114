#!python


__project__ = "alphatims"
__version__ = "0.2.8"
__license__ = "Apache"
__description__ = "A Python package to index Bruker TimsTOF raw data for fast and easy accession and visualization"
__author__ = "Sander Willems, Eugenia Voytik"
__author_email__ = "opensource@alphapept.com"
__github__ = "https://github.com/MannLabs/alphatims"
__keywords__ = [
    "ms",
    "mass spectrometry",
    "bruker",
    "timsTOF",
    "proteomics",
    "bioinformatics",
    "data indexing",
]
__python_version__ = ">=3.8,<3.9"
__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]
__console_scripts__ = [
    "alphatims=alphatims.cli:run",
]
__urls__ = {
    "Mann Labs at MPIB": "https://www.biochem.mpg.de/mann",
    "GitHub": __github__,
    "ReadTheDocs": "https://alphatims.readthedocs.io/en/latest/",
    "PyPi": "https://pypi.org/project/alphatims/",
    "Scientific paper": "https://doi.org/10.1101/2021.07.23.453379",
}
__requirements__ = {
    "": "requirements/requirements.txt",
    "stable": "requirements/requirements_stable.txt",
    "plotting": "requirements/requirements_plotting.txt",
    "development": "requirements/requirements_development.txt",
    "legacy": "requirements/requirements_legacy.txt",
}
__requirements_style__ = None
