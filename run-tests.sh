pydocstyle wtss_plugin/*.py wtss_plugin/dependencies/*.py wtss_plugin/dependencies/files_export/*.py setup.py && \
isort wtss_plugin setup.py --check-only --diff && \
check-manifest --ignore ".drone.yml,.readthedocs.yml" && \
sphinx-build -qnW --color -b doctest wtss_plugin/help/source wtss_plugin/help/_build && \
pytest