# Makefile for building the paper

.PHONY: all clean html pdf serve install build quick

all: html

# Quick build without executing notebooks
quick:
	jupyter-book build . --builder html -n

# Standard build - executes notebooks
build:
	jupyter-book build .

# Build HTML with execution
html:
	jupyter-book build . --all

# Build PDF (requires LaTeX)
pdf:
	jupyter-book build . --builder pdflatex

# Serve the built book locally
serve:
	cd _build/html && python -m http.server 8000

# Open the book in browser (MacOS)
open:
	open _build/html/index.html

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -e ..

# Clean build artifacts
clean:
	jupyter-book clean . --all
	rm -rf _build
	rm -f *.pdf

# Test the code
test-code:
	cd .. && pytest tests/ -v

# Update results notebook
update-results:
	jupyter nbconvert --execute --inplace 05_results.ipynb

# Check for broken links
check-links:
	jupyter-book build . --builder linkcheck

# Build everything from scratch
full-build: clean install test-code html
	@echo "Full build complete! Open _build/html/index.html to view."