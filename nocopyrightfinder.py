#!/usr/bin/python
# Copyright (c) 2010 Martin Ueding <dev@martin-ueding.de>

import os.path
import re
import sys

patterns = ['.*\\.java$', '.*\\.php$', '.*\\.cpp$', '.*\\.py$', '^makefile$', '.*\\.html$', '.*\\.js$', '.*\\.sh$', '.*\\.css$']
cPatterns = []
for pattern in patterns:
	cPatterns.append(re.compile(pattern))

copypattern1 = re.compile('.*Copyright \\(c\\)\\s?(\\d*) Martin Ueding \\<dev\\@martin-ueding\\.de\\>.*')
copypattern2 = re.compile('.*Martin Ueding.*')

good = []
bad = []

def checkFiles (arg, dirname, names):
	for name in names:
		path = dirname+'/'+name
		for pattern in cPatterns:
			if pattern.match(name) != None:
				copyright = 0
				year = ""

				with open(path, 'r') as script:
					for i in range(0, 5):
						line = script.readline()
						match = copypattern1.match(line)
						if match != None:
							copyright = 1
							year = match.group(1)

				if copyright == 1:
					good.append([path, year])
				else:
					bad.append(path)

os.path.walk('../../', checkFiles, 0)

if len(sys.argv) == 2 and sys.argv[1] == "-h":
	if len(bad) > 0:
		print "The following have no copyright notice:"
		for i in sorted(bad):
			print "-", i

		print

	if len(good) > 0:
		print "The following have a copyright notice:"
		for i in sorted(good):
			print "+", i[0], "("+i[1]+")"

	sum = len(good) + len(bad)

	print
	print "That are only "+str(len(good)*100/sum)+"% of your files."

elif len(sys.argv) == 2 and sys.argv[1] == "-g":
	for i in good:
		print i[0]
elif len(sys.argv) == 2 and sys.argv[1] == "-b":
	for i in bad:
		print i
else:
	for i in bad:
		print i
