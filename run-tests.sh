check-manifest --ignore ".drone.yml,.readthedocs.yml" && \
sphinx-build -qnW --color -b doctest wtss_plugin/help/source wtss_plugin/help/_build && \
pytest