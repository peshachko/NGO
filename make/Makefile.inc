DEPS =
VFLAGS =

MAKEFLAGS := --no-print-directory --warn-undefined-variables --no-builtin-rules
RUN = uv run --with=$(DEPS)

.PHONY: help

help: URL := github.com/drdv/makefile-doc/releases/latest/download/makefile-doc.awk
help: DIR := $(HOME)/.local/share/makefile-doc
help: SCR := $(DIR)/makefile-doc.awk
help: ## Show this help
	@test -f $(SCR) || wget -q -P $(DIR) $(URL)
	@awk $(VFLAGS) -f $(SCR) $(MAKEFILE_LIST)
