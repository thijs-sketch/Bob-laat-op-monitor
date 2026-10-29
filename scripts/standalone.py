import os, sys, glob, base64, re
root=sys.argv[1]; out=sys.argv[2]
html=open(os.path.join(root,"index.html"),encoding="utf-8").read()
blocks=[]
for f in sorted(glob.glob(os.path.join(root,"data","**","*.json"),recursive=True)):
    rel=os.path.relpath(f,root).replace(os.sep,"/")
    body=open(f,encoding="utf-8").read().replace("</","<"+chr(92)+"/")
    blocks.append('<script type="application/json" id="d:'+rel+'">'+body+'</script>')
marker='<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/'
def inline(m):
    f=os.path.join(root,m.group(1))
    return m.group(0).replace(m.group(1),"data:image/png;base64,"+base64.b64encode(open(f,"rb").read()).decode()) if os.path.exists(f) else m.group(0)
html=re.sub(r'(?:src|href)="(assets/[^"]+\.png)"',inline,html)
html=html.replace(marker,"\n".join(blocks)+"\n"+marker,1)
open(out,"w",encoding="utf-8").write(html); print(len(blocks),"files embedded,",round(os.path.getsize(out)/1e6,1),"MB")
