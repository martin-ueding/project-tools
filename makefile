# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.

# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.

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
