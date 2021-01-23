import io
import os

from setuptools import find_packages, setup

CURDIR = os.path.abspath(os.path.dirname(__file__))

DEPENDENCIES = ["beautifulsoup4==4.9.1",
                "bs4==0.0.1",
                "cltk==0.1.111",
                "greek-accentuation==1.2.0",
                "jupyter",
                "lxml",
                "matplotlib",
                "networkx==2.4",
                "norsecorpus==1.0.2",
                "notebook==6.1.5",
                "numpy==1.19.1",
                "requests==2.24.0",
                "scikit-learn==0.23.1",
                "scipy==1.4.1",
                "sigurd==1.2.9"]

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name='latechclfl2020besnier',
    version='1.0.2',
    url='https://www.clementbesnier.fr/dlh-vol-nib',
    license='Creative Commons Attribution 4.0 International Licence',
    author='Clément Besnier',
    author_email='clem@clementbesnier.fr',
    description='',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    keywords=["old-norse", "middle-high-german", "latin", "network analysis"],
    scripts=[],
    zip_safe=True,
    install_requires=DEPENDENCIES,
    test_suite="tests.test_project",
    python_requires=">=3.6",
    # license and classifier list:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
