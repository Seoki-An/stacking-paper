from pathlib import Path
import sys, shutil
import win32com.client
sys.path.insert(0, '.tmp/pdfdeps')
import pymupdf

root = Path.cwd()
src = root/'figures/.source/benchmarks-20261102'
work = root/'.tmp/benchmark-figures-20261102'
deck = src/'benchmark-figures-latex.pptx'
backup = root/'.backups/benchmark-figures-20261102/benchmark-before-seesaw-compact.pptx'
if not backup.exists():
    shutil.copy2(deck, backup)
app = win32com.client.Dispatch('PowerPoint.Application')
pres = next((p for p in app.Presentations if Path(p.FullName) == deck), None)
opened = pres is None
if opened:
    pres = app.Presentations.Open(str(deck), False, False, False)
slide = pres.Slides(1)
scene = slide.Shapes('Original seesaw trajectories (4800 x 1800)')
scene.LockAspectRatio = 0
scene.Left, scene.Top, scene.Width, scene.Height = 72, 0, 576, 216
for name, center in [('seesaw_structure', 216), ('seesaw_single', 504)]:
    shape = slide.Shapes(name)
    shape.Left, shape.Top = center - shape.Width/2, 224
pres.Save()
if opened:
    pres.Close()

# Preserve original pixels and vector labels without PowerPoint downsampling.
original = pymupdf.open(src/'pose_optimization_toy-source.pdf')
out = pymupdf.open()
page = out.new_page(width=720, height=252)
page.insert_image(pymupdf.Rect(72, 0, 648, 216), filename=str(src/'seesaw_trajectories.png'))
for clip, target in [((0,270,360,306),(36,216,396,252)),
                     ((360,270,720,306),(324,216,684,252))]:
    page.show_pdf_page(pymupdf.Rect(target), original, 0, clip=pymupdf.Rect(clip))
out.save(src/'pose_optimization_toy-compact-source.pdf', garbage=4, deflate=True)
page.get_pixmap(matrix=pymupdf.Matrix(2,2)).save(work/'seesaw-compact-preview.png')
print('Scene: 80%; original label scale preserved; figure height 306 -> 252 pt.')
