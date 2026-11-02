from pathlib import Path
import sys, shutil, json
import win32com.client
sys.path.insert(0,'.tmp/pdfdeps')
import pymupdf
root=Path.cwd();work=root/'.tmp/figure-adjust-20261102'
app=win32com.client.Dispatch('PowerPoint.Application')
pres=next(p for p in app.Presentations if Path(p.FullName)==root.parent/'figures/overview.pptx')
pres.SaveCopyAs(str(work/'overview-before.pptx'),24)
s=pres.Slides(1);sh={o.Id:o for o in s.Shapes}
dx=647-sh[106].Left
sh[106].Left=647;sh[106].Top=163
label=s.Shapes('Selected action (LaTeX vector)');label.Left+=dx;label.Top+=.9
sh[108].Left=594;sh[108].Top=171
sh[140].Delete();sh[141].Delete()
line=s.Shapes.AddLine(685.55,157.25,685.55,163)
line.Name='Action selection arrow';line.Line.Weight=1.25
line.Line.ForeColor.RGB=0;line.Line.EndArrowheadStyle=2
pres.Save();pres.SaveCopyAs(str(root/'figures/.source/overview/source.pptx'),24)
pres.SaveCopyAs(str(root/'.tmp/overview-20261102/updated-full.pdf'),32)

masks=[(129,51.8,138,55.8),(188,71.8,229.5,90),(234,77.5,241.5,83)]
pres=next(p for p in app.Presentations if Path(p.FullName)==root.parent/'figures/figures.pptx')
pres.SaveCopyAs(str(work/'figures-before-masks.pptx'),24)
s=pres.Slides(2)
for i,(x0,y0,x1,y1) in enumerate(masks):
    shape=s.Shapes.AddShape(1,589.146378+x0,213.121811+y0,x1-x0,y1-y0)
    shape.Name=f'Excavator mark mask {i+1}'
    shape.Fill.Solid();shape.Fill.ForeColor.RGB=0;shape.Line.Visible=0
pres.Save();pres.SaveCopyAs(str(root/'figures/.source/preliminary_result/source-masked.pptx'),24)
source=root/'figures/.source/preliminary_result'
backup=source/'before-masks.pdf'
if not backup.exists():shutil.copy2(root/'figures/preliminary_result.pdf',backup)
doc=pymupdf.open(backup)
for box in masks:doc[0].draw_rect(pymupdf.Rect(box),color=None,fill=(0,0,0),overlay=True)
doc.save(source/'masked-source.pdf',garbage=4,deflate=True)
doc[0].get_pixmap(matrix=pymupdf.Matrix(4,4)).save(work/'masked-preview.png')
(source/'mark-masks.json').write_text(json.dumps({'coordinates':'PDF points, top-left origin','rectangles':masks},indent=2))
print('Updated both PPT sources and added three opaque vector masks.')
