# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

git-tarball.1.gz: git-tarball.1
	gzip $<

%.1: %.1.rst
	rst2man $< $@

install:
	if [ -f git-tarball.1.gz ]; then install -d "$(DESTDIR)/usr/share/man/man1/"; install -m 644 git-tarball.1.gz -t "$(DESTDIR)/usr/share/man/man1/"; fi
	install -d "$(DESTDIR)/usr/bin/"
	install git-tarball -t "$(DESTDIR)/usr/bin/"

.PHONY: clean
clean:
	$(RM) git-tarball.1
	$(RM) git-tarball.1.gz
