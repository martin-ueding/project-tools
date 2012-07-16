# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all:
	@echo "Nothing to do."

install:
	install -d "$(DESTDIR)/usr/bin/"
	install create-bare -t "$(DESTDIR)/usr/bin/"
	install push-repo -t "$(DESTDIR)/usr/bin/"
