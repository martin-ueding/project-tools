# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

all:

install:
	install -d "$(DESTDIR)/usr/bin/"
	install prolint -t "$(DESTDIR)/usr/bin/"
	install prolint-report -t "$(DESTDIR)/usr/bin/"

clean:
