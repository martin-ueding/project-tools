#!/usr/bin/python
# Copyright (c) 2010 Martin Ueding <dev@martin-ueding.de>

import os.path
import re
import sys
import optparse
import readline

patterns = ['.*\\.java$', '.*\\.php$', '.*\\.cpp$', '.*\\.py$', '^makefile$', '.*\\.html$', '.*\\.js$', '.*\\.sh$', '.*\\.css$']
cPatterns = []
for pattern in patterns:
	cPatterns.append(re.compile(pattern))

def addcopyright(files):

	for f in files:
		print "working on", f

		lines = []
		with open(f) as handle:
			for line in handle:
				lines.append(line)

		for i, line in enumerate(lines[0:5]):
			print str(i+1), line,

		print "I will add a",
		comment = None
		newlineafter = True
		if cPatterns[3].match(f) != None or cPatterns[4].match(f) != None or cPatterns[7].match(f) != None:
			print "#",
			comment = "# %s"
		elif cPatterns[0].match(f) != None or cPatterns[2].match(f) != None or cPatterns[6].match(f) != None:
			print "//",
			comment = "// %s"
		elif cPatterns[8].match(f) != None:
			print "/* */",
			comment = "/* %s */"
		elif cPatterns[1].match(f) != None:
			print "<?PHP /* */ ?>",
			comment = "<?PHP /* %s */ ?>"
			newlineafter = False
		elif cPatterns[5].match(f) != None:
			print "<!-- -->",
			comment = "<!-- %s -->"
			newlineafter = False


		if comment == None:
			print "ERROR: no comment chosen"
			continue

		copyrightstring = "Copyright (c) Martin Ueding <dev@martin-ueding.de>"

		insertline = int(raw_input("Before which line should I insert the copyright info? ")) -1
		year_string = raw_input("In which year was this file created or last worked on? (leave empty if unsure) ")
		if len(year_string) > 0:
			copyrightstring = "Copyright (c) "+year_string+" Martin Ueding <dev@martin-ueding.de>"


		newfile = lines[:insertline] + [(comment+"\n") % copyrightstring]
		if newlineafter:
			newfile = newfile + ["\n"]
		
		newfile = newfile + lines[insertline:]

		print "This is going to be the new file"
		for i, line in enumerate(newfile[0:5]):
			print str(i+1), line,

		commit = raw_input("Do you want to write that out? [y/n] ")
		if commit == "y":
			with open(f, "w") as handle:
				for line in newfile:
					handle.write(line)

		print
		print "-----------------------------------------------"
		print


def main():
	parser = optparse.OptionParser("usage: %prog repository")
	parser.add_option("--human", dest="human", action="store_true", default=False, help="human readable output")
	parser.add_option("-g", dest="good", action="store_true", default=False, help="show only with copyright")
	parser.add_option("-b", dest="bad", action="store_true", default=False, help="show only files without copyright [default]")
	parser.add_option("--no-year", dest="noyear", action="store_true", default=False, help="show only files without a year in the copyright")
	parser.add_option("--add", dest="add", action="store_true", default=False, help="interactively add copyright to the files")
	parser.add_option("--relax", dest="relax", action="store_true", default=False, help="also accept second pattern")
	(options, args) = parser.parse_args()
	del parser

	if len(args) != 1:
		print "please supply a repository path with your files"
		sys.exit(1)

	
	ignorepatterns = []
	try:
		with open(os.path.expanduser("~/.nocopyrightfinder/ignore.txt")) as ifile:
			for line in ifile:
				ignorepatterns.append(line[:-1])
	except IOError:
		pass

	copypatterns = []
	try:
		with open(os.path.expanduser("~/.nocopyrightfinder/patterns.txt")) as patternfile:
			for line in patternfile:
				copypatterns.append(line[:-1])
	except IOError:
		print "file with copyright patterns could not be loaded"
		sys.exit(1)
			
	copypattern1 = re.compile(copypatterns[0])
	copypattern2 = re.compile(copypatterns[1])

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

								if options.relax:
									if copypattern2.match(line) != None:
										copyright = 1

						if copyright == 1:
							good.append([path, year])
						else:
							bad.append(path)

	os.path.walk(args[0], checkFiles, 0)

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

	elif options.add:
		addcopyright(bad)

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

if __name__ == "__main__":
	main()
