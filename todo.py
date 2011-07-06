#!/usr/bin/python
# Copyright (c) 2010 Martin Ueding <dev@martin-ueding.de>

import os.path
import re
import sys
import optparse
import readline
import time

patterns = ['.*\\.java$', '.*\\.php$', '.*\\.cpp$', '.*\\.py$', '^makefile$',
            '.*\\.html$', '.*\\.js$', '.*\\.sh$', '.*\\.css$']
cPatterns = []

words = ["(TODO .*)", "(HACK .*)", "(FIXME .*)", "(XXX .*)"]

commentpatterns = []
for w in words:
    commentpatterns.append("\\s+//\\s+"+w+"$")  
    commentpatterns.append("\\s+#\\s+"+w+"$")   
    commentpatterns.append("\\s+/\\*\\s+"+w+"\\*/$")    
    commentpatterns.append("\\s+<--\\s+"+w+"-->$")  

cCommentpatterns = []

ignorepatterns = []

for pattern in patterns:
    cPatterns.append(re.compile(pattern))

for pattern in commentpatterns:
    cCommentpatterns.append(re.compile(pattern))

def checkFiles (arg, dirname, names):
    for name in names:
        path = dirname+'/'+name

        if not any(ignore in path for ignore in ignorepatterns):

            for pattern in cPatterns:
                if pattern.match(name) is not None:

                    with open(path, 'r') as script:
                        nameprinted = False
                        for i, line in enumerate(script):
                            
                            for cc in cCommentpatterns:
                                match = cc.match(line)
                                if match is not None:
                                    if not nameprinted:
                                        print
                                        print path
                                        nameprinted = True
                                    print str(i).rjust(4), match.group(1)





def main():
    if os.path.exists("ignore.txt"):
        with open("ignore.txt") as ifile:
            for line in ifile:
                ignorepatterns.append(line[:-1])

    print "TODO List generated at",time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.localtime())
    
    os.path.walk('.', checkFiles, 0)

if __name__ == "__main__":
    main()
