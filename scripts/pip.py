import json
def rings(g):
    return g["coordinates"] if g["type"]=="Polygon" else [r for p in g["coordinates"] for r in p]
def polys(g):
    return [g["coordinates"]] if g["type"]=="Polygon" else g["coordinates"]
def inring(x,y,r):
    c=False; j=len(r)-1
    for i in range(len(r)):
        xi,yi=r[i][:2]; xj,yj=r[j][:2]
        if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi)+xi: c=not c
        j=i
    return c
class Index:
    def __init__(self, feats, key):
        self.items=[]
        for f in feats:
            xs=[p[0] for r in rings(f["geometry"]) for p in r]; ys=[p[1] for r in rings(f["geometry"]) for p in r]
            self.items.append((min(xs),min(ys),max(xs),max(ys),f["geometry"],f["properties"][key]))
    def find(self,x,y):
        for a,b,c,d,g,k in self.items:
            if a<=x<=c and b<=y<=d:
                for p in polys(g):
                    if inring(x,y,p[0]) and not any(inring(x,y,h) for h in p[1:]): return k
        return None
    def nearest(self,x,y):
        k=self.find(x,y)
        if k: return k
        best=min(self.items,key=lambda it:((it[0]+it[2])/2-x)**2+((it[1]+it[3])/2-y)**2); return best[5]
