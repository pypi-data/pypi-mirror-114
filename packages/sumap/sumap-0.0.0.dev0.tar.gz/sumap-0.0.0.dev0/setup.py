# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sumap',
    version='0.0.0.dev0',
    description='SUMAP: Supervised UMAP',
    long_description=readme,
    author='Tianlin He',
    author_email='tinaho_ok@hotmail.com',
    url='https://github.com/tianlinhe/sumap',
    license=license,
    packages=find_packages(exclude=('tests',
                                    'docs',
                                    'examples',
                                    'figures')),
    install_requires=[
        "numpy >= 1.17",
        "scikit-learn >= 0.22",
        "scipy >= 1.0",
        "numba >= 0.49",
        "pynndescent >= 0.5",
        ],
    )
