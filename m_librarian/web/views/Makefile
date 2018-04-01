.SUFFIXES: # Clear the suffix list
.SUFFIXES: .py .tmpl .html


%.py: %.tmpl
	cheetah compile --nobackup $< && compyle $@


templates = $(shell echo *.tmpl)
modules = $(patsubst %.tmpl,%.py,$(templates))


.PHONY: all
all: $(modules)
