# Where São Paulo's stages are

An interactive D3 map of São Paulo's 96 districts, colored by the number of theatre stages (or seats) in each one, with the theatre venues mapped on OpenStreetMap drawn on top.

**Live page:** https://clarabrandaog.github.io/sao-paulo-stages/

Four central districts (Bela Vista, República, Consolação and Santa Cecília) hold 128 of the city's 294 theatre stages, about 44%. 42 of the 96 districts have none.

## Data

| File | What it is | Source |
| --- | --- | --- |
| `data/districts.topo.json` | District boundaries with theatre counts joined in (rooms, seats, municipal / state / private rooms, OSM venues) | Boundaries: [GeoSampa](https://geosampa.prefeitura.sp.gov.br/) via [codigourbano/distritos-sp](https://github.com/codigourbano/distritos-sp). Counts: [Infocidade](https://prefeitura.sp.gov.br/licenciamento/w/desenvolvimento_urbano/dados_estatisticos/info_cidade/cultura/260233), *Salas de Teatro* 2017 (SMUL/Geoinfo, from the Secretaria Municipal de Cultura and the Guia da Folha) |
| `data/venues.json` | 85 theatre venues with coordinates and their district | [OpenStreetMap](https://www.openstreetmap.org/) (`amenity=theatre` inside the city), retrieved November 2026 via the Overpass API |

## Process

- `process/salas_2017.csv`: the 2017 Infocidade table as published.
- `process/build.py`: joins the table to the district shapes (`python3 build.py distritos-sp.geojson salas_2017.csv`).
- `process/osm_theatres.txt`: the raw Overpass result (117 entries).
- `process/venues.py`: drops unnamed points, non-theatres (a buffet, a samba school, circus tents, university lecture rooms) and duplicates, then assigns each venue to its district.
- Shapes were simplified to 8% in [mapshaper](https://mapshaper.org/) and converted to TopoJSON.

## Run locally

The page loads its data with `fetch`, so serve the folder instead of opening the file:

```
python3 -m http.server
```

Then open http://localhost:8000.

## Limits

The official counts are from 2017, the latest year published per district as a table; the venue layer is from 2026. OpenStreetMap is edited by volunteers and is incomplete (Teatro Santander, for example, is missing).

Clara Brandão, Parsons MFA Design and Technology.
