LATEX_PROCESSOR := pdflatex

LATEX_FLAGS :=
# LATEX_FLAGS := \def\showmargins{}

NOTES := $(basename $(wildcard *.tex))

OPEN_TARGETS = $(addprefix open-, $(NOTES))

help: URL := github.com/drdv/makefile-doc/releases/latest/download/makefile-doc.awk
help: DIR := $(HOME)/.local/share/makefile-doc
help: SCR := $(DIR)/makefile-doc.awk
help: VFLAG := -v SUB='$$(OPEN_TARGETS):open-:$(NOTES)'
help: ## Show this help
	@test -f $(SCR) || wget -q -P $(DIR) $(URL)
	@awk $(VFLAG) -f $(SCR) $(MAKEFILE_LIST)

## Generate all notes
all: $(addsuffix .pdf, $(NOTES))

%.pdf: %.tex Makefile
	@$(LATEX_PROCESSOR) "$(LATEX_FLAGS)\input{$<}"
	@$(LATEX_PROCESSOR) "$(LATEX_FLAGS)\input{$<}"

## Documents:
$(OPEN_TARGETS): open-%: %.pdf
	@xdg-open $< &

clean: ## Clean all PDF files
	@rm -f *.pdf *.log *.aux *.toc *.out
