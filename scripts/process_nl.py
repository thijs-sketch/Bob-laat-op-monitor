import json, sys, collections
sys.path.insert(0, sys.argv[1]); from pip import Index
R=sys.argv[2]+"/"; O=sys.argv[3]+"/"
L=lambda f: json.load(open(R+f))
st=lambda s: (s or "").strip()
def num(v): return v if isinstance(v,(int,float)) else None

prov=L("nl_prov2025.json")["features"]; pidx=Index(prov,"statnaam")
gpts={f["properties"]["statcode"]:f["geometry"]["coordinates"] for f in L("nl_gem_pts.json")["features"]}
gem=L("nl_gem2025.json"); gidx=Index(gem["features"],"statcode")
kwb25={st(r["WijkenEnBuurten"]):r for r in L("nl_kwb2025_gm.json")}
pv=collections.defaultdict(dict)
for r in L("nl_gem_pv_years.json")["value"]: pv[r["RegioS"].strip()][r["Perioden"][:4]]=(r["Installaties_1"],r["OpgesteldVermogenVanZonnepanelen_2"])
for f in gem["features"]:
    p=f["properties"]; c=p["statcode"]; k=kwb25.get(c,{}); y=pv.get(c,{})
    n25=y.get("2025",(None,None)); n22=y.get("2022",(None,None))
    won=num(k.get("Woningvoorraad_35"))
    f["properties"]={"id":c,"name":p["statnaam"],"land":"NL","prov":pidx.nearest(*gpts[c]),
        "pv":n25[0],"kwp":n25[1],"won":won,"pct":round(100*n25[0]/won,1) if n25[0] and won else None,
        "pv22":n22[0],"groei":round(100*(n25[0]/n22[0]-1)) if n25[0] and n22[0] else None,
        "trend":[y.get(str(j),(None,))[0] for j in range(2019,2026)],
        "woz":num(k.get("GemiddeldeWOZWaardeVanWoningen_39")),"koop":num(k.get("Koopwoningen_47")),"inw":num(k.get("AantalInwoners_5"))}
json.dump(gem,open(O+"nl_gem.json","w"))

pv22={st(r["WijkenEnBuurten"]):r for r in L("nl_wb_pv2022.json")}
k22={st(r["WijkenEnBuurten"]):r for r in L("nl_kwb2022.json")}
# map 2022 gemeente -> 2025 gemeente by majority of buurt points
votes=collections.defaultdict(collections.Counter)
for f in L("nl_buurt_pts.json")["features"]:
    x,y=f["geometry"]["coordinates"]; votes[f["properties"]["gemeentecode"]][gidx.nearest(x,y)]+=1
g22to25={g:c.most_common(1)[0][0] for g,c in votes.items()}
print("changed gemeenten:", {g:v for g,v in g22to25.items() if g!=v})
gprov={f["properties"]["id"]:f["properties"]["prov"] for f in gem["features"]}
def attrs(code):
    a=pv22.get(code,{}); k=k22.get(code,{})
    n=num(a.get("AantalInstallatiesBijWoningen_5")); won=num(k.get("Woningvoorraad_34"))
    return {"pv":n,"kwp":num(a.get("OpgesteldVermogenVanZonnepanelen_6")),"won":won,
        "pct":round(100*n/won,1) if n is not None and won and won>=10 else None,
        "woz":num(k.get("GemiddeldeWOZWaardeVanWoningen_35")),"koop":num(k.get("Koopwoningen_40")),
        "eengez":num(k.get("PercentageEengezinswoning_36")),"ink":num(k.get("GemiddeldInkomenPerInwoner_72")),
        "pc4":st(k.get("MeestVoorkomendePostcode_114")) or None}
for lay,codek,namek in [("wijk","wijkcode","wijknaam"),("buurt","buurtcode","buurtnaam")]:
    d=L(f"nl_{lay}.json")
    for f in d["features"]:
        p=f["properties"]; g25=g22to25.get(p["gemeentecode"],p["gemeentecode"])
        q={"id":p[codek],"name":p[namek],"gm":g25,"prov":gprov.get(g25)}
        if lay=="buurt": q["wk"]=p["wijkcode"]
        q.update(attrs(p[codek])); f["properties"]=q
    json.dump(d,open(O+f"nl_{lay}_attr.json","w")); print(lay,len(d["features"]))
