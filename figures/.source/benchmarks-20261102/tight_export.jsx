(function(){
var root = new Folder('E:/03 \uB17C\uBB38\uC791\uC131/04 RSS - Stone Stacking/latex');
var work = new Folder(root.fsName+'/.tmp/benchmark-figures-20261102');
var out = new Folder(root.fsName+'/figures');
var names=['mcts_example','initial_pose_sampling'];
var report=[];
for(var i=0;i<names.length;i++){
  var name=names[i];
  var suffix=name==='mcts_example'?'-source.pdf':'-revised-final.pdf';
  var doc=app.open(new File(work.fsName+'/'+name+suffix));
  if(name==='mcts_example') doc.artboards[0].artboardRect=[0,306,720,67];
  var eps=new EPSSaveOptions();
  eps.embedAllFonts=true;eps.embedLinkedFiles=true;eps.cmykPostScript=false;
  eps.saveMultipleArtboards=true;eps.artboardRange='1';
  doc.saveAs(new File(work.fsName+'/'+name+'-tight.eps'),eps);
  var pdf=new PDFSaveOptions();
  pdf.preserveEditability=false;pdf.colorDownsampling=0;pdf.grayscaleDownsampling=0;pdf.monochromeDownsampling=0;
  doc.saveAs(new File(out.fsName+'/'+name+'.pdf'),pdf);
  report.push(name+': '+doc.artboards[0].artboardRect);
  doc.close(SaveOptions.DONOTSAVECHANGES);
}
return report.join('\n');
})();
