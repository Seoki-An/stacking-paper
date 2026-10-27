MAIN := root

.PHONY: all watch clean distclean wordcount

all:
	latexmk $(MAIN).tex

watch:
	latexmk -pvc -view=none $(MAIN).tex

clean:
	latexmk -c $(MAIN).tex

distclean:
	latexmk -C $(MAIN).tex

wordcount:
	texcount -inc -total -sum $(MAIN).tex
