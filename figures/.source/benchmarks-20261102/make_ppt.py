from pathlib import Path
import sys, json, shutil
import win32com.client
sys.path.insert(0,'.tmp/pdfdeps')
from pypdf import PdfReader

root=Path.cwd()
work=root/'.tmp/benchmark-figures-20261102'
source=root/'figures/.source/benchmarks-20261102'
app=win32com.client.Dispatch('PowerPoint.Application')
pres=app.Presentations.Add(False)
pres.PageSetup.SlideWidth=720
pres.PageSetup.SlideHeight=306

def picture(slide,path,x,y,w,h,name):
    s=slide.Shapes.AddPicture(str(path),False,True,x,y,w,h)
    s.Name=name
    return s

def label(slide,name,center,y):
    page=PdfReader(work/(name+'.pdf')).pages[0]
    w,h=float(page.mediabox.width),float(page.mediabox.height)
    s=picture(slide,work/(name+'.svg'),center-w/2,y,w,h,name)
    s.AlternativeText=(work/(name+'.tex')).read_text()
    s.Title='LaTeX vector label'
    s.Tags.Add('LATEX_SOURCE',(work/(name+'.tex')).read_text())
    shutil.copy2(work/(name+'.svg'),source/(name+'.svg'))

slide=pres.Slides.Add(1,12)
picture(slide,source/'seesaw_trajectories.png',0,0,720,270,'Original seesaw trajectories (4800 x 1800)')
label(slide,'seesaw_structure',180,278)
label(slide,'seesaw_single',540,278)
slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text=(
    'Source: benchmarks/posegen-seesaw/seesaw.json and seesaw_trajectories.png. '
    'Left: structure-wide equilibrium; right: candidate-only equilibrium. '
    'Yellow: initial pose; green: optimized pose; gray: intermediate iterates. '
    'Original pixels retained. Labels compiled with pdflatex and dvisvgm; '
    'their editable TeX sources are stored in Alternative Text and adjacent .tex files.')
slide=pres.Slides.Add(2,12)
picture(slide,source/'mcts-art.svg',0,0,720,205.2/515.52*720,'Original vector wall comparison')
label(slide,'mcts_title',180,242)
label(slide,'greedy_title',540,242)
label(slide,'mcts_metric',180,277)
label(slide,'greedy_metric',540,277)
slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text=(
    'Source: benchmarks/wall-comparison/mcts_greedy.svg and numerical_results.json. '
    'Seed 6, same 49-stone inventory. MCTS: 19 stones, 43.9542% target filling; '
    'greedy: 14 stones, 36.0981%. This is a single recorded comparison, not an aggregate '
    'or equal-time benchmark. Dashed blue outlines show the target. '
    'Original vector geometry preserved; replacement labels compiled from LaTeX.')

dest=source/'benchmark-figures-latex.pptx'
pres.SaveAs(str(dest),24)
pres.SaveAs(str(work/'powerpoint-export.pdf'),32)
for i in (1,2):
    pres.Slides(i).Export(str(work/f'slide-{i}.png'),'PNG',1800,765)
pres.Close()
print('Saved two-slide PowerPoint with vector LaTeX labels and PDF export.')
