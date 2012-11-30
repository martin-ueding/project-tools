# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all:
	@echo "Nothing to do."

install:
	install -d "$(DESTDIR)/usr/bin/"
	install create-bare -t "$(DESTDIR)/usr/bin/"
	install git-push-chaos -t "$(DESTDIR)/usr/bin/"
	install git-push-github -t "$(DESTDIR)/usr/bin/"
