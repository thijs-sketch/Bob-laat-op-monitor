import json, sys, collections
R=sys.argv[1]+"/"; O=sys.argv[2]+"/"
L=lambda f: json.load(open(R+f))
PROV={"1":"Antwerpen","2":"Vlaams-Brabant","3":"West-Vlaanderen","4":"Oost-Vlaanderen","7":"Limburg"}
pv={x["postcode"]:x for x in L("be_pv_pc.json") if x["postcode"]}
bat={x["postcode"]:x for x in L("be_bat_pc.json") if x["postcode"]}
ean={x["postcode"]:x for x in L("be_ean_pc.json")}
gem=L("be_gem.json"); name2nis={f["properties"]["NAAM"].upper():f["properties"]["NISCODE"] for f in gem["features"]}
pcs={}
for pc in set(pv)|set(ean)|set(bat):
    e=ean.get(pc,{}); nis=name2nis.get(e.get("gem"))
    if not nis: continue
    n=pv.get(pc,{}).get("n",0); b=bat.get(pc,{}).get("n",0); a=e.get("n")
    pcs[pc]={"id":pc,"gm":"BE"+nis,"gmname":e["gem"].title(),"prov":PROV[nis[0]],"pv":n,"kwp":round(pv.get(pc,{}).get("kva",0)),
        "won":a,"pct":round(100*n/a,1) if a and a>=20 else None,"bat":b,"batkwh":round(bat.get(pc,{}).get("kwh",0)),
        "batpct":round(100*b/n,1) if n>=20 else None,"kans":max(n-b,0)}
json.dump(pcs,open(O+"be_pc_attr.json","w"))
agg=collections.defaultdict(lambda: collections.Counter())
for p in pcs.values():
    for k in ["pv","kwp","won","bat","batkwh","kans"]: agg[p["gm"]][k]+=p[k] or 0
for f in gem["features"]:
    p=f["properties"]; c="BE"+p["NISCODE"]; a=agg[c]
    f["properties"]={"id":c,"name":p["NAAM"],"land":"BE","prov":PROV[p["NISCODE"][0]],"pv":a["pv"],"kwp":a["kwp"],"won":a["won"],
        "pct":round(100*a["pv"]/a["won"],1) if a["won"] else None,"bat":a["bat"],"batkwh":a["batkwh"],
        "batpct":round(100*a["bat"]/a["pv"],1) if a["pv"] else None,"kans":a["kans"],
        "pcs":sorted(k for k,v in pcs.items() if v["gm"]==c)}
json.dump(gem,open(O+"be_gem.json","w"))
print(len(pcs), sum(p["pv"] for p in pcs.values()), sum(p["bat"] for p in pcs.values()))
top=sorted(gem["features"],key=lambda f:-(f["properties"]["pct"] or 0))[:3]; [print(f["properties"]) for f in top]
