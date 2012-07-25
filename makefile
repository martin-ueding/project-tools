# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all:
	@echo "Nothing to do. Call “make install”."

install:
	install -d "$(DESTDIR)/usr/bin/"
	install prolint -t "$(DESTDIR)/usr/bin/"

clean:
