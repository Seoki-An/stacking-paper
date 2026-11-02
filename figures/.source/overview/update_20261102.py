from pathlib import Path
import json, shutil
import win32com.client
from PIL import Image

root=Path.cwd(); work=root/'.tmp/overview-20261102'; src=root/'figures/.source/overview'
app=win32com.client.Dispatch('PowerPoint.Application')
pres=next(p for p in app.Presentations if Path(p.FullName)==root.parent/'figures/overview.pptx')
slide=pres.Slides(1)
shapes={s.Id:s for s in slide.Shapes}
shutil.copy2(work/'user-current.pptx',src/'before-update-20261102.pptx')
shutil.copy2(root.parent/'figures/overview/inventory.png',src/'inventory-original.png')
im=Image.open(src/'inventory-original.png')
im.crop((0,0,im.width,im.height*3//4)).save(src/'inventory-3x4.png')

# Keep the user's new state image and its aspect ratio; reduce image area only.
s=shapes[14]; cx=s.Left+s.Width/2
s.LockAspectRatio=-1; s.Width=s.Width*.90; s.Left=cx-s.Width/2
shapes[114].Top-=4.5
old=shapes[3]; old.Delete()
pic=slide.Shapes.AddPicture(str(src/'inventory-3x4.png'),False,True,0,102.25,56,42)
pic.Left=252.5428-28; pic.Name='Inventory 3x4 (original pixels)'
pic.Line.Visible=-1; pic.Line.Weight=.35; pic.Line.ForeColor.RGB=0
shapes[16].Top=147.5
shapes[13].Height=119.1
shapes[15].Top=160.5

# Compact only the lower return loop and result box, keeping label sizes.
shapes[9].Height-=6
shapes[10].Height-=6
shapes[101].Height-=6
shapes[99].Top-=6
shapes[100].Top-=6
shapes[108].Top-=6
box=shapes[106]; box.Top=162.1; box.Height=14.5
label=shapes[107]
tex=label.Tags.Item('LATEXADDIN').replace('Selected validated \\\\\n','Selected ')
# Keep the original LaTeX font and IguanaTeX size; remove the line break.
tex=label.Tags.Item('LATEXADDIN').replace('Selected validated', 'Selected').replace('\\\\', '')
label.Tags.Add('LATEXADDIN',tex)
label.Tags.Add('BITMAPVECTOR','1')
pres.Windows(1).Activate(); app.ActiveWindow.View.GotoSlide(1)
label.Select()
app.Run('IguanaTex_v1_58.ppam!RegenerateSelectedDisplays')
label=app.ActiveWindow.Selection.ShapeRange(1)
label.Name='Selected action (IguanaTeX vector)'
label.Left=box.Left+(box.Width-label.Width)/2
label.Top=box.Top+(box.Height-label.Height)/2
(src/'selected-action.tex').write_text(tex)
pres.Save()
pres.SaveCopyAs(str(src/'source.pptx'),24)
pres.SaveCopyAs(str(work/'updated-full.pdf'),32)
slide.Export(str(work/'after.png'),'PNG',2400,1350)
records=[]
for s in slide.Shapes:
    records.append({'id':s.Id,'name':s.Name,'type':s.Type,'x':s.Left,'y':s.Top,'w':s.Width,'h':s.Height})
(work/'updated-shapes.json').write_text(json.dumps(records,indent=2))
print('Saved updated overview and editable source; selected label dimensions:',label.Width,label.Height)
