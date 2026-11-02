from pathlib import Path
import sys, shutil, json
import win32com.client
sys.path.insert(0,'.tmp/pdfdeps')
from pypdf import PdfReader
import pymupdf

root=Path.cwd(); work=root/'.tmp/benchmark-figures-20261102'; source=root/'figures/.source/benchmarks-20261102'
shutil.copy2(source/'benchmark-figures-latex.pptx',root/'.backups/benchmark-figures-20261102/benchmark-figures-before-label-revision.pptx')
doc=pymupdf.open(work/'initial_pose_sampling-source.pdf')
page=doc[0]
page.add_redact_annot(pymupdf.Rect(0,162,515.52,180),fill=False)
page.apply_redactions(images=0,graphics=0,text=0)
doc.save(work/'sampling-unlabeled.pdf',garbage=4,deflate=True)
doc.close()

app=win32com.client.Dispatch('PowerPoint.Application')
pres=app.Presentations.Open(str(source/'benchmark-figures-latex.pptx'),False,False,True)
slide=pres.Slides(2)
for name in ('mcts_metric','greedy_metric'):
    slide.Shapes(name).Delete()
for name in ('mcts_title','greedy_title'):
    slide.Shapes(name).Top=207

slide=pres.Slides.Add(3,12)
im=slide.Shapes.AddPicture(str(root.parent/'figures/initial-pose-sampling/proposal_pipeline.png'),False,True,0,0,720,180/515.52*720)
im.Name='Sampling scene preview (original pixels)'
mask=slide.Shapes.AddShape(1,0,162/515.52*720,720,306-162/515.52*720)
mask.Fill.ForeColor.RGB=16777215
mask.Line.Visible=False
mask.Name='Hide original embedded panel labels'
pres.Windows(1).Activate()
app.ActiveWindow.View.GotoSlide(3)
records=[]
for name,center in [('sampling_a',120),('sampling_b',351),('sampling_c',586)]:
    p=PdfReader(work/(name+'.pdf')).pages[0]
    w,h=float(p.mediabox.width),float(p.mediabox.height)
    shape=slide.Shapes.AddPicture(str(work/(name+'.svg')),False,True,center-w/2,238,w,h)
    shape.Name=name
    tex=(work/(name+'.tex')).read_text()
    tags={'LATEXADDIN':tex,'IGUANATEXSIZE':'10','IGUANATEXCURSOR':str(len(tex)),
          'TRANSPARENCY':'True','FILENAME':'','LATEXENGINEID':'1','BITMAPVECTOR':'1',
          'ORIGINALHEIGHT':str(h),'ORIGINALWIDTH':str(w),'OUTPUTDPI':'1200'}
    for key,value in tags.items(): shape.Tags.Add(key,value)
    shape.Select()
    app.Run('IguanaTex_v1_58.ppam!RegenerateSelectedDisplays')
    updated=app.ActiveWindow.Selection.ShapeRange(1)
    updated.Name=name
    updated.Left=center-updated.Width/2
    updated.Top=238
    records.append({'name':name,'type':updated.Type,'width':updated.Width,'height':updated.Height,
                    'bitmap_vector':updated.Tags.Item('BITMAPVECTOR'),
                    'latex_source':updated.Tags.Item('LATEXADDIN')})
    print('IguanaTeX regenerated '+name,flush=True)
    shutil.copy2(work/(name+'.tex'),source/(name+'.tex'))
    shutil.copy2(work/(name+'.svg'),source/(name+'.svg'))

slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text=(
    'Sampling source: project figures/initial-pose-sampling/proposal_pipeline.pdf. '
    'Panel labels are separate native IguanaTeX vector displays, regenerated with '
    'the installed IguanaTex_v1_58 add-in. Use Edit LaTeX display to change them. '
    'The final EPS preserves original PDF geometry instead of the raster preview used here.')
pres.Save()
pres.SaveAs(str(work/'powerpoint-revised.pdf'),32)
for i in (2,3): pres.Slides(i).Export(str(work/f'revised-slide-{i}.png'),'PNG',1800,765)
pres.Close()
(source/'iguanatex-label-audit.json').write_text(json.dumps(records,indent=2))
print('Revised PPT saved, including three regenerated IguanaTeX labels.',flush=True)
