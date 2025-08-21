# Makefile for building the paper

.PHONY: all clean html pdf serve install

all: html pdf

install:
	pip install -r requirements.txt
	pip install -e ..

html:
	jupyter-book build . --all

pdf: html
	jupyter-book build . --builder pdflatex

serve:
	cd _build/html && python -m http.server

clean:
	jupyter-book clean . --all
	rm -rf _build
	rm -f *.pdf

test-code:
	cd .. && pytest tests/ -v

update-results:
	jupyter nbconvert --execute --inplace 05_results.ipynb

check-links:
	jupyter-book build . --builder linkcheck

# Build everything from scratch
full-build: clean install test-code html pdf
	@echo "Full build complete!"