import sys, io, zipfile, zlib, json
from pathlib import Path
sys.path.insert(0, '.tmp/pdfdeps')
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject, EncodedStreamObject, RectangleObject
from PIL import Image

source_dir = Path('figures/source/overview')
source = source_dir / 'source.pptx'
z = zipfile.ZipFile(source)
writer = PdfWriter(clone_from=source_dir / 'full.pdf')
page = writer.pages[0]
xobjects = page['/Resources']['/XObject']
mapping = dict(zip(range(1, 23), list(range(14, 50, 2)) + [52, 54, 56, 58]))
mapping.update({23:60,24:62,25:66,26:68,27:70,28:72,29:74,30:78,31:80,32:84,33:87})
audit = []
for media_index, object_index in mapping.items():
    image = Image.open(io.BytesIO(z.read(f'ppt/media/image{media_index}.png'))).convert('RGBA')
    original_size = image.size
    if media_index == 32:
        w,h = image.size
        image = image.crop((0, round(h*.25521), w, round(h*(1-.03031))))
    if media_index == 33:
        w,h = image.size
        image = image.crop((round(w*.38125), round(h*.241), round(w*(1-.05307)), round(h*(1-.19327))))
    obj = xobjects[f'/Image{object_index}'].get_object()
    old_size = [int(obj['/Width']), int(obj['/Height'])]
    assert abs((image.width/image.height)/(old_size[0]/old_size[1])-1) < .08, (media_index, old_size, image.size)
    obj.clear()
    obj.update({NameObject('/Type'):NameObject('/XObject'), NameObject('/Subtype'):NameObject('/Image'),
        NameObject('/Width'):NumberObject(image.width),NameObject('/Height'):NumberObject(image.height),
        NameObject('/BitsPerComponent'):NumberObject(8),NameObject('/ColorSpace'):NameObject('/DeviceRGB'),
        NameObject('/Filter'):NameObject('/FlateDecode')})
    obj._data = zlib.compress(image.convert('RGB').tobytes())
    if image.getchannel('A').getextrema() != (255,255):
        mask = EncodedStreamObject()
        mask.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Image'),
            NameObject('/Width'):NumberObject(image.width),NameObject('/Height'):NumberObject(image.height),
            NameObject('/BitsPerComponent'):NumberObject(8),NameObject('/ColorSpace'):NameObject('/DeviceGray'),
            NameObject('/Filter'):NameObject('/FlateDecode')})
        mask._data = zlib.compress(image.getchannel('A').tobytes())
        obj[NameObject('/SMask')] = writer._add_object(mask)
    audit.append({'source':f'image{media_index}.png','original':original_size,'exported':old_size,'restored':image.size})
page.mediabox = RectangleObject([209,345,790,506])
page.cropbox = RectangleObject([209,345,790,506])
writer.write('figures/overview.pdf')
(source_dir / 'image-audit.json').write_text(json.dumps(audit,indent=2))
print(f'Restored {len(audit)} embedded originals without resampling; source crops preserved.')
