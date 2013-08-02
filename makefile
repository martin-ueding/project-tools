# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

all:

install:
	install -d "$(DESTDIR)/usr/bin/"
	install create-bare -t "$(DESTDIR)/usr/bin/"
	install git-init-bitbucket -t "$(DESTDIR)/usr/bin/"
	install git-init-chaos -t "$(DESTDIR)/usr/bin/"
	install git-init-default -t "$(DESTDIR)/usr/bin/"
	install git-init-github -t "$(DESTDIR)/usr/bin/"

clean:
