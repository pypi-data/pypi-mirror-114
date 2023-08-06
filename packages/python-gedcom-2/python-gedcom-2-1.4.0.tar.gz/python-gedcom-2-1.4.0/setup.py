from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the `README.md` file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-gedcom-2',
    version='1.4.0',
    description='A Python module for parsing, analyzing, and manipulating GEDCOM files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/swanny0819/python-gedcom',
    author='Patrick Swanson',
    author_email='patswanson+python_gedcom@gmail.com',
    license='GPLv2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Sociology :: Genealogy',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='python gedcom parser',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
    extras_require={
        'dev': ['setuptools', 'wheel', 'twine', 'pdoc3'],
        'test': ['tox'],
    },
    package_data={},
    data_files=[],
    project_urls={
        'Bug Reports': 'https://github.com/swanny0819/python-gedcom/issues',
        'Source': 'https://github.com/swanny0819/python-gedcom',
    },
)
