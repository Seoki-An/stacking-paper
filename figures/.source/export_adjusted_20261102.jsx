(function(){
var root=new Folder('E:/03 \uB17C\uBB38\uC791\uC131/04 RSS - Stone Stacking/latex');
var prior=app.userInteractionLevel;
app.userInteractionLevel=UserInteractionLevel.DONTDISPLAYALERTS;
var specs=[['overview','overview/updated-20261102.pdf',525,149],
           ['preliminary_result','preliminary_result/masked-source.pdf',246.222,134.963]];
var report=[];
try{
for(var i=0;i<specs.length;i++){
 var s=specs[i];var doc=app.open(new File(root.fsName+'/figures/.source/'+s[1]));
 doc.artboards[0].artboardRect=[0,s[3],s[2],0];
 var opt=new EPSSaveOptions();opt.embedAllFonts=true;opt.embedLinkedFiles=true;
 opt.cmykPostScript=false;opt.saveMultipleArtboards=true;opt.artboardRange='1';
 doc.saveAs(new File(root.fsName+'/.tmp/figure-adjust-20261102/'+s[0]+'.eps'),opt);
 doc.close(SaveOptions.DONOTSAVECHANGES);report.push(s[0]+' exported');
}
}finally{app.userInteractionLevel=prior;}
return report.join('\n');
})();
