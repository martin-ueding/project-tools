#!/usr/bin/python
# Copyright (c) 2010 Martin Ueding <dev@martin-ueding.de>

import os.path
import re
import sys
import optparse

parser = optparse.OptionParser("usage: %prog")
parser.add_option("--human", dest="human", action="store_true", default=False, help="human readable output")
parser.add_option("-g", dest="good", action="store_true", default=False, help="show only with copyright")
parser.add_option("-b", dest="bad", action="store_true", default=False, help="show only files without copyright [default]")
parser.add_option("--no-year", dest="noyear", action="store_true", default=False, help="show only files without a year in the copyright")
parser.add_option("--add", dest="add", action="store_true", default=False, help="interactively add copyright to the files")
(options, args) = parser.parse_args()
del parser

patterns = ['.*\\.java$', '.*\\.php$', '.*\\.cpp$', '.*\\.py$', '^makefile$', '.*\\.html$', '.*\\.js$', '.*\\.sh$', '.*\\.css$']
cPatterns = []
for pattern in patterns:
	cPatterns.append(re.compile(pattern))

ignorepatterns = []
with open("ignore.txt") as ifile:
	for line in ifile:
		ignorepatterns.append(line[:-1])

copypattern1 = re.compile('.*Copyright \\(c\\)\\s?(\\d*) Martin Ueding \\<dev\\@martin-ueding\\.de\\>.*')
copypattern2 = re.compile('.*Martin Ueding.*')

good = []
bad = []

def checkFiles (arg, dirname, names):
	for name in names:
		path = dirname+'/'+name

		if not any(ignore in path for ignore in ignorepatterns):

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

if options.human:
	good.sort()
	bad.sort()
	if len(bad) > 0:
		print "The following have no copyright notice:"
		for i in bad:
			print "-", i

		print

	if len(good) > 0:
		print "The following have a copyright notice but no year:"
		for i in good:
			if i[1] == "":
				print "+", i[0], "("+i[1]+")"

		print "The following have a copyright notice:"
		for i in good:
			if i[1] != "":
				print "+", i[0], "("+i[1]+")"

	sum = len(good) + len(bad)

	print
	print str(len(good)*100/sum)+"% of your files have a copyright"

elif options.good:
	for i in good:
		print i[0]
elif options.bad:
	for i in bad:
		print i
elif options.noyear:
	for i in good:
		if i[1] == "":
			print i[0]
else:
	for i in bad:
		print i
