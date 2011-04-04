#!/bin/bash
# Copyright (c) 2011 Martin Ueding <dev@martin-ueding.de>

# get a list of all the files that have my copyright in them
./nocopyrightfinder.py ../.. -g --relax > good

echo "	files	lines	chars"

for suffix in java php css js html py sh cpp c
do
	lines=$(cat `cat good | egrep "\\.$suffix$"` | wc -l)
	chars=$(cat `cat good | egrep "\\.$suffix$"` | wc -m)
	echo "$suffix	`egrep "\\.$suffix$" good | wc -l`	$lines	$chars"
done

lines=$(cat `cat good | egrep "makefile$"` | wc -l)
chars=$(cat `cat good | egrep "makefile$"` | wc -m)
echo "make	`egrep "makefile$" good | wc -l`	$lines	$chars"

rm good

