#
# This file is part of Python QGIS Plugin for WTSS.
# Copyright (C) 2024 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Python QGIS Plugin for WTSS."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('docs/CHANGES.rst').read()

docs_require = [
    'Sphinx>=2.2',
    'sphinx_rtd_theme',
    'sphinx-copybutton'
]

dev_env_require = [
    'pb-tool>=3.0.0'
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
    'dev': dev_env_require,
    'tests': tests_require
}

extras_require['all'] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = [
    'pytest-runner>=5.2'
]

install_requires = [
    'numpy>=1.19',
    'matplotlib>=3.3.3',
    'pandas>=1.1',
    'jsonschema>=3.2.0',
    'wtss>=0.7.0'
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
    license='GPLv3',
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
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: GIS',
    ]
)
