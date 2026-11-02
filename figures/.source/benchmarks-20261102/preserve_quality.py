from pathlib import Path
import sys, zlib, json, shutil
sys.path.insert(0,'.tmp/pdfdeps')
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import NameObject, NumberObject, ContentStream
from PIL import Image

work=Path('.tmp/benchmark-figures-20261102')
source=Path('figures/.source/benchmarks-20261102')
export=PdfReader(work/'powerpoint-export.pdf')
writer=PdfWriter()
page=writer.add_page(export.pages[0])
images=[v.get_object() for v in page['/Resources']['/XObject'].values()
        if v.get_object().get('/Subtype')=='/Image']
assert len(images)==1
original=Image.open(source/'seesaw_trajectories.png').convert('RGB')
image=images[0]
old=[int(image['/Width']),int(image['/Height'])]
image.clear()
image.update({NameObject('/Type'):NameObject('/XObject'),
    NameObject('/Subtype'):NameObject('/Image'),
    NameObject('/Width'):NumberObject(original.width),
    NameObject('/Height'):NumberObject(original.height),
    NameObject('/BitsPerComponent'):NumberObject(8),
    NameObject('/ColorSpace'):NameObject('/DeviceRGB'),
    NameObject('/Filter'):NameObject('/FlateDecode')})
image._data=zlib.compress(original.tobytes())
writer.write(work/'pose_optimization_toy-source.pdf')

# Preserve the exact original vector scene, avoiding PowerPoint's SVG
# tessellation seams. The transforms and LaTeX labels match slide 2.
art=PdfWriter(clone_from='../figures/benchmarks/wall-comparison/mcts_greedy.pdf')
art.remove_text()
writer=PdfWriter()
page=writer.add_blank_page(720,306)
scale=720/515.52
page.merge_transformed_page(art.pages[0],Transformation().scale(scale).translate(0,306-205.2*scale))
labels=export.pages[1]
stream=ContentStream(labels.get_contents(),export)
ops=stream.operations
first_end=next(i for i,(_,op) in enumerate(ops) if op==b'EMC')
base_name=next(args[0] for args,op in ops if op==b'Do')
stream.operations=[(args,op) for args,op in ops[first_end+1:]
                   if not (op==b'Do' and args[0]==base_name)]
labels[NameObject('/Contents')]=stream
del labels['/Resources']['/XObject'][base_name]
page.merge_page(labels)
writer.write(work/'mcts_example-source.pdf')

shutil.copy2('../figures/initial-pose-sampling/proposal_pipeline.pdf',work/'initial_pose_sampling-source.pdf')
audit={'seesaw_export_pixels':old,'seesaw_restored_pixels':list(original.size),
       'mcts_scene':'original vector PDF; only old text removed',
       'labels':'pdflatex + dvisvgm SVG in PowerPoint; source TeX and SVG retained',
       'sampling_source':'../figures/initial-pose-sampling/proposal_pipeline.pdf'}
(source/'quality-audit.json').write_text(json.dumps(audit,indent=2))
print(json.dumps(audit))
