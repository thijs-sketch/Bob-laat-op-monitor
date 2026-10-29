import json, sys, urllib.request
url, out = sys.argv[1], sys.argv[2]
rows=[]
while url:
    d=json.load(urllib.request.urlopen(url, timeout=300))
    rows+=d["value"]; url=d.get("odata.nextLink")
json.dump(rows, open(out,"w")); print(out, len(rows))
