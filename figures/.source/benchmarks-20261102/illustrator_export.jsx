(function(){
var base = new Folder("E:/03 \ub17c\ubb38\uc791\uc131/04 RSS - Stone Stacking/latex");
var work = new Folder(base.fsName + '/.tmp/benchmark-figures-20261102');
var out = new Folder(base.fsName + '/figures');
var names = ['pose_optimization_toy', 'mcts_example', 'initial_pose_sampling'];
var report = [];
var prior = app.userInteractionLevel;
app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
var stage = 'start';
try {
  for (var i = 0; i < names.length; i++) {
    var name = names[i];
    stage = 'open ' + name;
    var suffix = name === 'initial_pose_sampling' ? '-revised-final.pdf' : '-source.pdf';
    var doc = app.open(new File(work.fsName + '/' + name + suffix));
    var fonts = [];
    for (var j = doc.textFrames.length - 1; j >= 0; j--) {
      fonts.push(doc.textFrames[j].textRange.characterAttributes.textFont.name);
      doc.textFrames[j].createOutline();
    }
    var eps = new EPSSaveOptions();
    eps.embedAllFonts = true;
    eps.embedLinkedFiles = true;
    eps.includeDocumentThumbnails = false;
    eps.cmykPostScript = false;
    stage = 'save ' + name;
    doc.saveAs(new File(out.fsName + '/' + name + '.eps'), eps);
    var pdf = new PDFSaveOptions();
    pdf.preserveEditability = false;
    pdf.generateThumbnails = false;
    pdf.colorDownsampling = 0;
    pdf.grayscaleDownsampling = 0;
    pdf.monochromeDownsampling = 0;
    stage = 'save ' + name;
    doc.saveAs(new File(out.fsName + '/' + name + '.pdf'), pdf);
    report.push(name + ': rasterItems=' + doc.rasterItems.length +
                '; pathItems=' + doc.pathItems.length + '; outlinedFonts=' + fonts.join(','));
    doc.close(SaveOptions.DONOTSAVECHANGES);
  }
} catch(err) { report.push(stage + ' ERROR ' + err); } finally {
  app.userInteractionLevel = prior;
}
report.join('\n');

return report.join('\n');
})();
