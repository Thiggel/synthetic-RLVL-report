LATEXMK ?= latexmk
MAIN ?= main.tex

.PHONY: all clean

all:
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(MAIN)

clean:
	$(LATEXMK) -C $(MAIN)
