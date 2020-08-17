NAME=receiptparser
VERSION=`python3 setup.py --version | sed s/^v//`
PREFIX=/usr/local/
BIN_DIR=$(PREFIX)/bin
SITE_DIR=$(PREFIX)`python3 -c "from __future__ import print_function; import sys; from distutils.sysconfig import get_python_lib; print(get_python_lib()[len(sys.prefix):])"`

###################################################################
# Standard targets.
###################################################################
.PHONY : clean
clean:
	find . -name "*.pyc" -o -name "*.pyo" | xargs -n1 rm -f
	rm -Rf build *.egg-info

.PHONY : dist-clean
dist-clean: clean
	rm -Rf dist

install:
	mkdir -p $(SITE_DIR)
	./version.sh
	export PYTHONPATH=$(SITE_DIR):$(PYTHONPATH); \
	python3 setup.py install --prefix $(PREFIX) \
	                        --install-scripts $(BIN_DIR) \
	                        --install-lib $(SITE_DIR)
	./version.sh --reset

uninstall:
	# Sorry, Python's distutils support no such action yet.

.PHONY : tests
tests:
	cd tests/Exscript/; ./run_suite.py 1

###################################################################
# Package builders.
###################################################################
targz: clean
	./version.sh
	python3 setup.py sdist --formats gztar
	./version.sh --reset

tarbz: clean
	./version.sh
	python3 setup.py sdist --formats bztar
	./version.sh --reset

wheel: clean
	./version.sh
	python3 setup.py bdist_wheel --universal
	./version.sh --reset

deb: clean
	./version.sh
	debuild -S -sa
	cd ..; sudo pbuilder build $(NAME)_$(VERSION)-0ubuntu1.dsc; cd -
	./version.sh --reset

dist: targz tarbz wheel

###################################################################
# Publishers.
###################################################################
dist-publish:
	./version.sh
	twine upload dist/*
	./version.sh --reset
