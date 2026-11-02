from pathlib import Path
import json, shutil, sys, xml.etree.ElementTree as ET
sys.path.insert(0, '.tmp/pdfdeps')
from pypdf import PdfReader

work = Path('.tmp/benchmark-figures-20261102')
source = Path('figures/.source/benchmarks-20261102')
assets = Path('../figures/benchmarks')
labels = {
    'seesaw_structure': r'(a) Structure-wide',
    'seesaw_single': r'(b) Candidate-only',
    'mcts_title': r'(a) MCTS',
    'greedy_title': r'(b) Greedy',
    'mcts_metric': r'19 stones; 44.0\% target coverage',
    'greedy_metric': r'14 stones; 36.1\% target coverage',
}
for name, text in labels.items():
    fontsize = 24 if 'metric' not in name else 19
    tex = r'''\documentclass[border=1pt]{standalone}
\usepackage{amsmath,mathptmx}
\begin{document}
\fontsize{SIZE}{LEADING}\selectfont TEXT
\end{document}
'''.replace('SIZE',str(fontsize)).replace('LEADING',str(fontsize+3)).replace('TEXT',text)
    (work / (name+'.tex')).write_text(tex)
    (source / (name+'.tex')).write_text(tex)

svg = ET.parse(assets/'wall-comparison/mcts_greedy.svg')
for parent in svg.getroot().iter():
    for node in list(parent):
        if node.get('id','').startswith('text_'):
            parent.remove(node)
ET.register_namespace('', 'http://www.w3.org/2000/svg')
svg.write(work/'mcts-art.svg',encoding='utf-8',xml_declaration=True)
shutil.copy2(assets/'posegen-seesaw/seesaw_trajectories.png',source/'seesaw_trajectories.png')
shutil.copy2(work/'mcts-art.svg', source/'mcts-art.svg')
shutil.copy2(assets/'posegen-seesaw/seesaw.json',source/'seesaw.json')
shutil.copy2(assets/'wall-comparison/numerical_results.json',source/'numerical_results.json')
(source/'labels.json').write_text(json.dumps(labels,indent=2))
print('Prepared original figure assets and six LaTeX labels.')
