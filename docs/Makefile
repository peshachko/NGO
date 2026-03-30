include ../make/Makefile.inc
include ../make/Makefile_tex.inc

FILE :=
GENDER := f

# LATEX_FLAGS := \def\showmargins{}

## Устав и учредителен протокол
ngo-creation-docs: $(BUILD_DIR)/creation/устав.pdf $(BUILD_DIR)/creation/учредителен-протокол.pdf

## Заявление за членство
# Should use xelatex in order to embed a font that has full Cyrillic coverage into the PDF.
# Otherwise there are problems e.g., when filling the application on mobile
# Requires:
#   sudo dnf install dejavu-fonts-all
application-tex: | $(BUILD_DIR)
	xelatex -output-directory=build заявление_членство.tex

## Show application fields
application-show:
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE is not defined. Usage: make application-show FILE=<your_file>"; \
		exit 1; \
	fi
	@uv run --with=pymupdf ../utils/application.py show $(FILE)

## Fill application fields (male)
application-fill-m: GENDER:=m
application-fill-m: application-fill

## Fill application fields (female)
application-fill-f: GENDER:=f
application-fill-f: application-fill

application-fill:
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE is not defined. Usage: make application-show FILE=<your_file>"; \
		exit 1; \
	fi
	@uv run --with=pymupdf ../utils/application.py fill -m -g $(GENDER) $(FILE)

clean: ## Clean build directory
	@rm -rf build
