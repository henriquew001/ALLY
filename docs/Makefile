# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = .
SOURCEDIR     = .
BUILDDIR      = _build

all: html

html:
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR) $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR) $(O)

.PHONY: clean html
