import json, sys, urllib.request, concurrent.futures as cf
W="https://service.pdok.nl/cbs/wijkenbuurten/2022/wfs/v1_0?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&srsName=EPSG:4326&count=1000&sortBy=gemeentecode"
layer, props, out = sys.argv[1], sys.argv[2], sys.argv[3]
def page(i):
    u=f"{W}&typeNames=wijkenbuurten:{layer}&propertyName={props},geom&startIndex={i*1000}"
    return json.load(urllib.request.urlopen(u, timeout=300))["features"]
feats=[]
with cf.ThreadPoolExecutor(6) as ex:
    for fs in ex.map(page, range(int(sys.argv[4]))): feats+=fs
feats=[f for f in feats if f["properties"].get("water")=="NEE" and f["geometry"]]
seen=set(); uniq=[]
for f in feats:
    k=json.dumps(f["properties"],sort_keys=True)
    if k not in seen: seen.add(k); uniq.append(f)
json.dump({"type":"FeatureCollection","features":uniq}, open(out,"w"))
print(layer, len(feats), len(uniq))
