from setuptools import setup
import setuptools
from pathlib import Path

# readme description
this_directory = Path(__file__).parent
long_description = (this_directory / "docs/index.md").read_text()

# libraries
requirements = [
    'pandas>=1.0.0',
]

setup(
    name='timewarpy',
    version='0.0.16',
    description='Time series processing framework and utilities for deep learning',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Clay Elmore',
    packages=setuptools.find_packages(),
    license='BSD 3-Clause License',
    include_package_data=True,
    install_requires=requirements,
    scripts=[],
    zip_safe=False
)
