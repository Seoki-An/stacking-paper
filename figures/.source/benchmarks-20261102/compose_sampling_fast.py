import sys
from pathlib import Path
sys.path.insert(0,'.tmp/pdfdeps')
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject
import pymupdf
work=Path('.tmp/benchmark-figures-20261102')
r=PdfReader(work/'powerpoint-revised.pdf');p=r.pages[2]
c=ContentStream(p.get_contents(),r);ops=c.operations
first_end=next(i for i,(_,op) in enumerate(ops) if op==b'EMC')
base=next(args[0] for args,op in ops if op==b'Do')
c.operations=[(args,op) for args,op in ops[first_end+1:] if not(op==b'Do' and args[0]==base)]
p[NameObject('/Contents')]=c
del p['/Resources']['/XObject'][base]
w=PdfWriter();w.add_page(p);w.write(work/'sampling-labels-only.pdf')
out=pymupdf.open();page=out.new_page(width=720,height=272)
art=pymupdf.open(work/'sampling-unlabeled-outlined.pdf')
page.show_pdf_page(pymupdf.Rect(0,0,720,180/515.52*720),art,0)
labels=pymupdf.open(work/'sampling-labels-only.pdf')
page.show_pdf_page(pymupdf.Rect(0,0,720,306),labels,0)
out.save(work/'initial_pose_sampling-revised-final.pdf',garbage=4,deflate=True)
page.get_pixmap(matrix=pymupdf.Matrix(2,2)).save(str(work/'sampling-final-source.png'))
print('Sampling scene and independent IguanaTeX vector labels composed.')
