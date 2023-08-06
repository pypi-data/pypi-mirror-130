from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Dimensionality Reduction in extreme regions'

# Setting up
setup(
    name="TIREX",
    version=VERSION,
    author="Anass Aghbalou",
    author_email="anass.aghbalou@hotmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['scikit-learn'],
    keywords=['python', 'Dimensionality reduction', 'Large/extreme values', 'Machine learning','regression','anomaly detection'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
