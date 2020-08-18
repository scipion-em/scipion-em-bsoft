"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

from bsoft import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='scipion-em-bsoft',  # Required
    version=__version__,  # Required
    description='Plugin to use Cryoef program within the Scipion framework',  # Required
    long_description=long_description,  # Optional
    url='https://github.com/scipion-em/scipion-em-bsoft',  # Optional
    author='I2PC',  # Optional
    author_email='scipion@cnb.csic.es',  # Optional
    keywords='scipion electron-microscopy cryo-em structural-biology image-processing scipion-3.0',  # Optional
    packages=find_packages(),
    install_requires=['scipion-em'],
    package_data={  # Optional
       'bsoft': ['bsoft_logo.png', 'protocols.conf'],
    },
    entry_points={
        'pyworkflow.plugin': 'bsoft = bsoft'
    },
)
