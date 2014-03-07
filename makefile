# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>

SHELL = /bin/bash

all:

.PHONY: clean
clean:
	$(RM) doc/*.1
	$(RM) doc/*.1.gz
	$(RM) -r build
	$(RM) -r dist
	$(RM) -r *.egg-info

install:
	install -d "$(DESTDIR)/usr/bin/"
	for script in bin/*; \
		do \
		install "$$script" -t "$(DESTDIR)/usr/bin/"; \
		done
#
	./setup.py install
