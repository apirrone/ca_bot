filename = inverse_kinematics
variable = $(filename).tex

all: pdflatex

pdflatex: $(variable)
	pdflatex $(variable)
	bibtex $(filename)
	pdflatex $(variable)
	pdflatex $(variable)

clean:
	rm $(filename).aux $(filename).pdf $(filename).glo $(filename).gls $(filename).bbl $(filename).log $(filename).blg $(filename).dvi $(filename).out $(filename).toc

show: pdflatex
	evince $(filename).pdf

