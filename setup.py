import os
from setuptools import find_packages, setup

install_requires = [
    'matplotlib',
    'wtss'
]

packages = find_packages()

g = {}
with open(os.path.join('wtss_plugin', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='wtss-qgis-plugin',
    version=version,
    keywords=['Web Time Series Service', 'Time series'],
    license='MIT',
    author='INPE',
    author_email='brazildatacube@dpi.inpe.br',
    url='https://github.com/brazil-data-cube/wtss',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={},
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License'
    ]
)