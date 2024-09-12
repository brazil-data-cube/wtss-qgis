from pathlib import Path

lib_paths = []

import json

lib_paths.append(json.__file__)

import numpy

lib_paths.append(numpy.__file__)

import seaborn

lib_paths.append(seaborn.__file__)

import matplotlib

lib_paths.append(matplotlib.__file__)

import pandas

lib_paths.append(pandas.__file__)

import jsonschema

lib_paths.append(jsonschema.__file__)

import pystac_client

lib_paths.append(pystac_client.__file__)

import wtss

lib_paths.append(wtss.__file__)

file = open(Path('scripts') / 'lib-paths.txt','w')
for path in lib_paths:
	file.write(str(path).replace('__init__.py', '') + "\n")
file.close()
