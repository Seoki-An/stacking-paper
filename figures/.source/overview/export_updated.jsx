(function(){
var root=new Folder('E:/03 \uB17C\uBB38\uC791\uC131/04 RSS - Stone Stacking/latex');
var doc=app.open(new File(root.fsName+'/figures/.source/overview/updated-20261102.pdf'));
doc.artboards[0].artboardRect=[0,149,525,0];
var eps=new EPSSaveOptions();eps.embedAllFonts=true;eps.embedLinkedFiles=true;
eps.cmykPostScript=false;eps.saveMultipleArtboards=true;eps.artboardRange='1';
doc.saveAs(new File(root.fsName+'/.tmp/overview-20261102/overview.eps'),eps);
var pdf=new PDFSaveOptions();pdf.preserveEditability=false;
pdf.colorDownsampling=0;pdf.grayscaleDownsampling=0;pdf.monochromeDownsampling=0;
doc.saveAs(new File(root.fsName+'/figures/overview.pdf'),pdf);
doc.close(SaveOptions.DONOTSAVECHANGES);
return 'Overview exported at 525 x 149 pt.';
})();
