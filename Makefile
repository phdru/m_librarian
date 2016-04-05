
.PHONY: all
all:
	@echo "Nothing to be done for 'all'"

.PHONY: htmldoc
htmldoc:
	$(MAKE) -C docs html
	$(MAKE) -C docs-ru html

.PHONY: test
test:
	$(MAKE) -C tests

.PHONY: tests
tests: test
