
.PHONY: all
all:
	@echo "Nothing to be done for 'all'"

.PHONY: htmldoc
htmldoc:
	$(MAKE) -C doc html
	$(MAKE) -C doc-ru html

.PHONY: test
test:
	$(MAKE) -C tests
