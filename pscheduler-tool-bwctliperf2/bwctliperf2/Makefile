#
# Makefile for any tool class
#

NAME=bwctliperf2

FILES=\
	can-run \
	duration \
	enumerate \
	merged-results \
	participant-data \
	run \
	iperf_parser.py \
	iperf_defaults.py\


DOCS=\
	$(NAME).txt




install: $(FILES) $(DOCS)
ifndef DESTDIR
	@echo No DESTDIR specified for installation
	@false
endif
ifdef DOCS
ifndef DOCDIR
	@echo No DOCDIR specified for installation
	@false
endif
endif
	mkdir -p $(DESTDIR)
	install -m 555 $(FILES) $(DESTDIR)
ifdef DOCS
	mkdir -p $(DOCDIR)
	install -m 444 $(DOCS) $(DOCDIR)
endif



clean:
	rm -f $(TO_CLEAN) *~
