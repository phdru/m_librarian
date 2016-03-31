
.PHONY: all
all:
	@echo "Nothing to be done for 'all'"

.PHONY: htmldoc
htmldoc:
	PYTHONPATH="`pwd`" $(MAKE) -C doc html
	PYTHONPATH="`pwd`" $(MAKE) -C doc-ru html
