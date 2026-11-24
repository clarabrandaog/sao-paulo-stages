import csv, json, unicodedata, sys
def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().upper()
    return s.replace('/', '-').strip()
def num(v):
    v = v.strip()
    return 0 if v in ('-', '') else int(v.replace('.', ''))

geo = json.load(open(sys.argv[1]))
feats = {norm(f['properties']['ds_nome']): f for f in geo['features']}
sub_districts = {}
for f in geo['features']:
    sub_districts.setdefault(norm(f['properties']['ds_subpref']), set()).add(norm(f['properties']['ds_nome']))

rows = list(csv.reader(open(sys.argv[2], encoding='utf-8')))[2:]  # skip header + MSP
alias = {'MOOCA': 'MOOCA'}
data, remaining, sub = {}, set(), None
for r in rows:
    name = norm(r[0])
    if not remaining:
        sub = name; sub_label = r[0].strip()
        if sub not in sub_districts:
            m = [k for k in sub_districts if k.startswith(sub)]
            if len(m) != 1: sys.exit(f'unknown subpref {sub}')
            sub = m[0]
        remaining = set(sub_districts[sub]); continue
    if name not in remaining: sys.exit(f'{name} not in {sub}: {remaining}')
    remaining.discard(name)
    data[name] = dict(label=r[0].strip(), subpref_label=sub_label, rooms=num(r[1]), seats=num(r[2]), municipal=num(r[3]), state=num(r[5]), private=num(r[7]))
assert len(data) == 96, len(data)
print('rooms', sum(d['rooms'] for d in data.values()), 'seats', sum(d['seats'] for d in data.values()))

out_rows = []
for key, f in feats.items():
    p = f['properties']; d = data[key]
    d = dict(d); lab = d.pop('label'); sl = d.pop('subpref_label')
    p2 = dict(id=p['ds_codigo'], name=lab, subprefecture=sl, **d)
    f['properties'] = p2
    out_rows.append(p2)
json.dump(geo, open('districts_theatres.geojson', 'w'))
out_rows.sort(key=lambda x: -x['rooms'])
with open('theatres_by_district_2017.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out_rows[0])); w.writeheader(); w.writerows(out_rows)
zero = sum(1 for x in out_rows if x['rooms'] == 0)
print('districts with zero rooms:', zero)
for x in out_rows[:10]: print(x['name'], x['rooms'], x['seats'])
