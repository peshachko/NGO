include ../make/Makefile.inc
include ../make/Makefile_tex.inc

# LATEX_FLAGS := \def\showmargins{}

## Устав и учредителен протокол
ngo-creation-docs: $(BUILD_DIR)/creation/устав.pdf $(BUILD_DIR)/creation/учредителен-протокол.pdf

## Заявление за членство
# Should use xelatex in order to embed a font that has full Cyrillic coverage into the PDF.
# Otherwise there are problems e.g., when filling the application on mobile
# Requires:
#   sudo dnf install dejavu-fonts-all
application-form: | $(BUILD_DIR)
	xelatex -output-directory=build заявление_членство.tex

clean: ## Clean build directory
	@rm -rf build
