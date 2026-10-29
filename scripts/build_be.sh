#!/bin/bash
set -e
# Gebruik: scripts/build_be.sh <werkmap>  (werkmap bevat raw/osm/, build/ en tools/ met mapshaper en osmtogeojson)
S="${1:?werkmap ontbreekt}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
MS=$S/tools/node_modules/.bin/mapshaper; OUT="$REPO/data/be"
cd $S/raw/osm
for f in *.; do $S/tools/node_modules/.bin/osmtogeojson "$f" > "$S/build/osm_$f.geojson"; done
cd $S/build
python3 - <<'PY'
import json, glob, unicodedata, re
slug=lambda s: re.sub(r'[^a-z]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
attrs=json.load(open('be_pc_attr.json')); by={}; seen=set()
for fn in sorted(glob.glob('osm_*.geojson')):
    for f in json.load(open(fn))['features']:
        pc=f['properties'].get('postal_code')
        if f['geometry']['type'] not in ('Polygon','MultiPolygon') or pc not in attrs or pc in seen: continue
        seen.add(pc); a=attrs[pc]
        by.setdefault(slug(a['prov']),[]).append({'type':'Feature','properties':a,'geometry':f['geometry']})
for p,fs in by.items(): json.dump({'type':'FeatureCollection','features':fs},open(f'split_be_{p}.json','w'))
print('postcodes with geometry',len(seen),'of',len(attrs),'missing',sorted(set(attrs)-seen))
PY
for P in antwerpen vlaams-brabant west-vlaanderen oost-vlaanderen limburg; do
  $MS -i split_be_$P.json -rename-layers pc -clip be_gem.json -simplify 12% keep-shapes -o "$OUT/$P.json" format=topojson quantization=100000 2>&1 | grep -v "^\[o\]" || true
done
ls -la "$OUT"
