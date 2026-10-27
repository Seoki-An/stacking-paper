# Build root.tex with pdflatex + bibtex (RSS template: IEEEtran + natbib/plainnat)
@default_files = ('root.tex');
$pdf_mode = 1;
$bibtex_use = 2;
$pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$clean_ext = 'bbl synctex.gz run.xml';
