#!/bin/bash
cd "$1"
for c in "1[5-9][0-9]{2}" "2[0-4][0-9]{2}" "2[5-9][0-9]{2}" "3[0-4][0-9]{2}" "3[5-9][0-9]{2}" "8[0-4][0-9]{2}" "8[5-9][0-9]{2}" "9[0-4][0-9]{2}" "9[5-9][0-9]{2}"; do
  f="chunk_${c:0:1}${c:1:5}.json"; f=$(echo "$f" | tr -d '[]-{}'); w=15
  for a in 1 2 3 4 5 6 7 8; do
    curl -s -m 300 -A "BobLaadtOp-solarmap/1.0" https://overpass-api.de/api/interpreter --data-urlencode "data=[out:json][timeout:240];rel[\"boundary\"=\"postal_code\"][\"postal_code\"~\"^$c\$\"](50.6,2.5,51.55,5.95);out geom;" -o "$f"
    if head -c 20 "$f" | grep -q '{'; then echo "$c ok $(wc -c < $f)"; break; fi
    echo "$c retry $a wait $w"; sleep $w; w=$((w*2>240?240:w*2))
  done
  sleep 5
done
echo done
