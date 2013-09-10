# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

SHELL = /bin/bash

rst_files = $(wildcard doc/*.?.rst)
man_pages = $(rst_files:.rst=.gz)

all: $(man_pages)

.PHONY: clean
clean:
	$(RM) doc/*.1
	$(RM) doc/*.1.gz

install:
	install -d "$(DESTDIR)/usr/bin/"
	for script in bin/*; \
		do \
		install "$$script" -t "$(DESTDIR)/usr/bin/"; \
		done
#
	install -d "$(DESTDIR)/usr/bin/"
	for manpage in doc/*.gz; \
		do \
		install -d "$(DESTDIR)/usr/share/man/man1/"; \
		install "$$manpage" -m 644 -t "$(DESTDIR)/usr/share/man/man1/"; \
		done

%.1.gz: %.1
	$(RM) $@
	gzip $<

%.1: %.1.rst
	rst2man $< $@
