from pathlib import Path
import sys, zipfile, io, json, posixpath, zlib
from xml.etree import ElementTree as ET
from PIL import Image
sys.path.insert(0,'.tmp/pdfdeps')
import pymupdf
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject, EncodedStreamObject, ContentStream
root=Path.cwd(); src=root/'figures/.source/overview'; work=root/'.tmp/overview-20261102'
z=zipfile.ZipFile(src/'source.pptx')
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
rels=ET.fromstring(z.read('ppt/slides/_rels/slide1.xml.rels'))
targets={r.attrib['Id']:posixpath.normpath('ppt/slides/'+r.attrib['Target']) for r in rels}
xml=ET.fromstring(z.read('ppt/slides/slide1.xml'))
pics=[]
for p in xml.findall('.//p:pic',ns):
    blip=p.find('p:blipFill/a:blip',ns); xf=p.find('p:spPr/a:xfrm',ns)
    if blip is None or xf is None:continue
    path=targets[blip.attrib['{'+ns['r']+'}embed']]
    if not path.endswith(('.png','.jpg','.jpeg')):continue
    off=xf.find('a:off',ns); ext=xf.find('a:ext',ns)
    x,y,w,h=[int(v)/12700 for v in (off.attrib['x'],off.attrib['y'],ext.attrib['cx'],ext.attrib['cy'])]
    im=Image.open(io.BytesIO(z.read(path))).convert('RGBA')
    crop=p.find('p:blipFill/a:srcRect',ns)
    if crop is not None:
        l,t,r,b=[int(crop.attrib.get(k,0))/100000 for k in ('l','t','r','b')]
        im=im.crop((round(im.width*l),round(im.height*t),round(im.width*(1-r)),round(im.height*(1-b))))
    pics.append((pymupdf.Rect(x,y,x+w,y+h),im,path))
doc=pymupdf.open(work/'updated-full.pdf'); page=doc[0]; audit=[]
reader=PdfReader(work/'updated-full.pdf')
writer=PdfWriter(clone_from=reader)
objects={v.idnum:v.get_object() for v in writer.pages[0]['/Resources']['/XObject'].values()}
# Use resource names to map the reader's object IDs to cloned writer objects.
objects={reader.pages[0]['/Resources']['/XObject'].raw_get(key).idnum:value.get_object()
         for key,value in writer.pages[0]['/Resources']['/XObject'].items()}
stream=ContentStream(writer.pages[0].get_contents(),writer)
resources=writer.pages[0]['/Resources']['/XObject']
draws=[args for args,op in stream.operations if op==b'Do' and resources[args[0]].get('/Subtype')=='/Image']
infos=page.get_image_info(xrefs=True)
assert len(draws)==len(infos),(len(draws),len(infos))
for index,(info,args) in enumerate(zip(infos,draws)):
    box=pymupdf.Rect(info['bbox'])
    matches=sorted(((sum(abs(a-b) for a,b in zip(box,rect)),im,path) for rect,im,path in pics),key=lambda a:a[0])
    if not matches or matches[0][0]>.8:continue
    error,im,path=matches[0]
    obj=EncodedStreamObject()
    def image_dict(mode):
        return {NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Image'),
                NameObject('/Width'):NumberObject(im.width),NameObject('/Height'):NumberObject(im.height),
                NameObject('/BitsPerComponent'):NumberObject(8),NameObject('/ColorSpace'):NameObject(mode),
                NameObject('/Filter'):NameObject('/FlateDecode')}
    obj.update(image_dict('/DeviceRGB')); obj._data=zlib.compress(im.convert('RGB').tobytes())
    if im.getchannel('A').getextrema()!=(255,255):
        mask=EncodedStreamObject(); mask.update(image_dict('/DeviceGray'))
        mask._data=zlib.compress(im.getchannel('A').tobytes())
        obj[NameObject('/SMask')]=writer._add_object(mask)
    name=NameObject('/Restored'+str(index)); resources[name]=writer._add_object(obj);args[0]=name
    audit.append({'source':path,'exported':[info['width'],info['height']],'restored':list(im.size),'bbox':list(box)})
writer.pages[0][NameObject('/Contents')]=writer._add_object(stream)
writer.write(work/'restored-full.pdf')
doc=pymupdf.open(work/'restored-full.pdf');page=doc[0]
page.set_cropbox(pymupdf.Rect(209,34,734,183))
out=pymupdf.open(); dest=out.new_page(width=525,height=149)
dest.show_pdf_page(dest.rect,doc,0)
out.save(src/'updated-20261102.pdf',garbage=4,deflate=True)
dest.get_pixmap(matrix=pymupdf.Matrix(3,3)).save(work/'restored-preview.png')
(src/'updated-image-audit.json').write_text(json.dumps(audit,indent=2))
print('Restored',len(audit),'source pictures; cropped figure 525 x 149 pt.')
