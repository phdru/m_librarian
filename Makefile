
.PHONY: all
all:
	@echo "Nothing to be done for 'all'"

.PHONY: release
release: tests flake8 docs distr

.PHONY: distr
distr:
	./mk-distr

.PHONY: flake8
flake8:
	flake8

.PHONY: docs
docs: html

.PHONY: html
html:
	$(MAKE) -C docs html
	$(MAKE) -C docs-ru html

.PHONY: test
test:
	$(MAKE) -C tests

.PHONY: tests
tests: test

.PHONY: clean
clean:
	find . -name '*.py[co]' -type f -delete
