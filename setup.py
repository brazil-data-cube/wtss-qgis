#
# This file is part of Python QGIS Plugin for Web Time Series Services.
# Copyright (C) 2019-2020 INPE.
#
# Python QGIS Plugin for Web Time Series Services is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('CHANGES.rst').read()

docs_require = [
    'Sphinx>=2.2',
    'sphinx_rtd_theme',
    'sphinx-copybutton',
]

tests_require = [
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'isort>4.3',
    'check-manifest>=0.40'
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
}

extras_require['all'] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'pyproj>=2.5.0',
    'pyqt5-tools>=5.15',
    'pb-tool>=3.0.0',
    'numpy>=1.19',
    'matplotlib>=3.3.3',
    'pandas>=1.1',
]

packages = find_packages()

g = {}
with open(os.path.join('wtss_plugin', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='wtss_plugin',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    long_description_content_type = 'text/x-rst',
    keywords=['Time Series Service', 'GIS', 'QGIS'],
    license='MIT',
    author='Brazil Data Cube Team',
    author_email='brazildatacube@inpe.br',
    url='https://github.com/brazil-data-cube/wtss-qgis',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={},
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: GIS',
    ],
)