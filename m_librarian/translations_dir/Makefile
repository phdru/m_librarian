%.mo: %.po
	msgfmt -o $@ -- $<

po_files = $(shell echo *.po)
mo_files = $(patsubst %.po,%.mo,$(po_files))

.PHONY: all
all: $(mo_files)
