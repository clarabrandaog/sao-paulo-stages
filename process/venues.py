import json, csv
from shapely.geometry import shape, Point
geo = json.load(open('districts_theatres.geojson'))
polys = [(shape(f['geometry']), f['properties']) for f in geo['features']]
DROP_NAMES = {'Zoopaloo Buffet','Escola de Samba Colorado do Bras','Patati Patatá Circo Show','Circo Spacial',
  'Azul','Vermelho','Verde','Teatro','Auditório Milton Santos','Auditório Nicolau Sevcenko',
  'Anfiteatro da Geografia','Anfiteatro da História','Anfiteatros CB','Centro de Eventos Vila Mariana'}
FIX = {'Treato Sesc Avenida Paulista':'Teatro Sesc Avenida Paulista','Teadro Viradalata':'Teatro Viradalata',
       'Cacilda Becker':'Teatro Cacilda Becker','Teatro Clementica de Jesus':'Teatro Clementina de Jesus'}
out, seen, dropped = [], {}, []
for line in open('raw/osm_theatres.txt', encoding='utf-8'):
    oid, lat, lon, name, op, cap, wd = line.rstrip('\n').split('|')
    name = FIX.get(name, name)
    if not name or name in DROP_NAMES: dropped.append(name or oid); continue
    lat, lon = float(lat), float(lon)
    if name in seen and abs(seen[name][0]-lat)+abs(seen[name][1]-lon) < 0.01:
        dropped.append(name+' (duplicate)'); continue
    seen[name] = (lat, lon)
    pt = Point(lon, lat)
    d = next((p for g, p in polys if g.contains(pt)), None)
    if not d: dropped.append(name+' (outside city)'); continue
    out.append(dict(osm_id=oid, name=name, lat=round(lat,6), lon=round(lon,6), district_id=d['id'],
                    district=d['name'], operator=op, capacity=int(cap) if cap else None, wikidata=wd))
print(len(out), 'venues kept;', len(dropped), 'dropped:', dropped)
json.dump(out, open('venues_osm.json','w'), ensure_ascii=False, indent=1)
with open('venues_osm.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
# add venue counts to districts
cnt = {}
for v in out: cnt[v['district_id']] = cnt.get(v['district_id'],0)+1
for f in geo['features']: f['properties']['osm_venues'] = cnt.get(f['properties']['id'],0)
json.dump(geo, open('districts_theatres.geojson','w'))
from collections import Counter
print(Counter(v['district'] for v in out).most_common(8))
print('districts with venues:', len(cnt))
