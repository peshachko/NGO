NOTE =
BUILD_DIR := build
LATEX_PROCESSOR := pdflatex -output-directory=$(BUILD_DIR)
LATEX_FLAGS :=

.PHONY: tex open

## Procss a specific NOTE
tex: | $(BUILD_DIR)
	@$(LATEX_PROCESSOR) "$(LATEX_FLAGS)\input{$(NOTE).tex}"
	@$(LATEX_PROCESSOR) "$(LATEX_FLAGS)\input{$(NOTE).tex}"

$(BUILD_DIR)/%.pdf: %.tex | $(BUILD_DIR)
	$(LATEX_PROCESSOR) "$(LATEX_FLAGS)\input{$<}"
	$(LATEX_PROCESSOR) "$(LATEX_FLAGS)\input{$<}"

open:
	xdg-open $(BUILD_DIR)/$(NOTE).pdf &

$(BUILD_DIR):
	mkdir -p $@
