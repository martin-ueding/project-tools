#!/bin/bash
# Copyright (c) 2011 Martin Ueding <dev@martin-ueding.de>

# get a list of all the files that have my copyright in them
./nocopyrightfinder.py -g > good

echo "	files	lines"

for suffix in sh php java py js html
do
	lines=$(cat `cat good | egrep "\\.$suffix$"` | wc -l)
	echo "$suffix	`egrep "\\.$suffix$" good | wc -l`	$lines"
done

rm good

