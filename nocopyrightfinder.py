#!/usr/bin/python
# Copyright (c) 2010 Martin Ueding <dev@martin-ueding.de>

import os.path
import re

patterns = ['.*\\.java$', '.*\\.php$', '.*\\.cpp$', '.*\\.py$', '^makefile$', '.*\\.html$', '.*\\.js$']
cPatterns = []
for pattern in patterns:
	cPatterns.append(re.compile(pattern))

copypattern1 = re.compile('.*Copyright \\(c\\)\\s?\\d* Martin Ueding \\<dev\\@martin-ueding\\.de\\>.*')
copypattern2 = re.compile('.*Martin Ueding.*')

good = []
bad = []

def checkFiles (arg, dirname, names):
	for name in names:
		path = dirname+'/'+name
		for pattern in cPatterns:
			if pattern.match(name) != None:
				copyright = 0

				with open(path, 'r') as script:
					for i in range(0, 5):
						line = script.readline()
						if copypattern1.match(line) != None:
							copyright = 1

				if copyright == 1:
					good.append(path)
				else:
					bad.append(path)

os.path.walk('../../', checkFiles, 0)

for i in sorted(bad):
	print i

