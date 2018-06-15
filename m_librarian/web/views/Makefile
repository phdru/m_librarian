.SUFFIXES: # Clear the suffix list
.SUFFIXES: .py .tmpl .html


%.py: %.tmpl
	cheetah compile --nobackup $<
	python    -m compile $@
	python -O -m compile $@


templates = $(shell echo *.tmpl)
modules = $(patsubst %.tmpl,%.py,$(templates))


.PHONY: all
all: $(modules)
