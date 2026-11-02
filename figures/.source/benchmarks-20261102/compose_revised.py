from pathlib import Path
import sys, json
sys.path.insert(0,'.tmp/pdfdeps')
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import NameObject, ContentStream, RectangleObject
import pymupdf

work=Path('.tmp/benchmark-figures-20261102')
source=Path('figures/.source/benchmarks-20261102')
export=PdfReader(work/'powerpoint-revised.pdf')

def overlay_without_background(page, remove_first=False):
    stream=ContentStream(page.get_contents(),export)
    ops=stream.operations
    first_end=next(i for i,(_,op) in enumerate(ops) if op==b'EMC')
    objects=page['/Resources'].get('/XObject',{})
    omit={key for key,val in objects.items() if val.get_object().get('/Subtype')=='/Image'}
    if remove_first:
        omit.add(next(args[0] for args,op in ops if op==b'Do'))
    stream.operations=[(args,op) for args,op in ops[first_end+1:]
                       if not (op==b'Do' and args[0] in omit)]
    page[NameObject('/Contents')]=stream
    for key in omit:
        del objects[key]
    return page

art=PdfWriter(clone_from='../figures/benchmarks/wall-comparison/mcts_greedy.pdf')
art.remove_text()
w=PdfWriter(); page=w.add_blank_page(720,306)
scale=720/515.52
page.merge_transformed_page(art.pages[0],Transformation().scale(scale).translate(0,306-205.2*scale))
page.merge_page(overlay_without_background(export.pages[1],remove_first=True))
page.mediabox=RectangleObject([0,67,720,306]);page.cropbox=page.mediabox
w.write(work/'mcts_example-source.pdf')

w=PdfWriter();page=w.add_blank_page(720,306)
art=PdfReader(work/'sampling-unlabeled-outlined.pdf').pages[0]
page.merge_transformed_page(art,Transformation().scale(scale).translate(0,306-180*scale))
page.merge_page(overlay_without_background(export.pages[2]))
page.mediabox=RectangleObject([0,34,720,306]);page.cropbox=page.mediabox
w.write(work/'initial_pose_sampling-outlined.pdf')
for name in ['mcts_example-source','initial_pose_sampling-outlined']:
    doc=pymupdf.open(work/(name+'.pdf'))
    doc[0].get_pixmap(matrix=pymupdf.Matrix(2,2)).save(str(work/(name+'-revised.png')))
print('Composed final vector scenes with the revised PowerPoint labels.')
