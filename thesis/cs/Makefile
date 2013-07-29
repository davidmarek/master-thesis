all: thesis.pdf
	cp thesis.pdf ../..

# Vyroba PDF primo z DVI by byla prijemnejsi, ale vetsina verzi dvipdfm nici obrazky
# thesis.pdf: thesis.dvi
#	dvipdfm -o $@ -p a4 -r 600 $<

thesis.pdf: thesis.tex $(wildcard *.tex) citace.bib mysphinx.sty
	pdflatex $<
	bibtex thesis
	pdflatex $<
	pdflatex $<
#	ps2pdf $< $@

clean:
	rm -f *.bbl *.blg *.log *.dvi *.aux *.toc *.lof *.out thesis.ps thesis.pdf thesis.dvi
