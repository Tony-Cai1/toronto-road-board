# Toronto Road Board — V1

A tiny Flask app that renders two saved Toronto road restrictions. V1 deliberately labels every record **Road closed**. That is correct for the full closure and wrong for the lane restriction, preserving the observed behavior for the first Aurora incident.

The app never calls the network at runtime. It loads [`data/road_restrictions.json`](data/road_restrictions.json).

## Data provenance

- City service query page requested for this work: <https://gis.toronto.ca/arcgis/rest/services/cot_geospatial2/FeatureServer/5/query>
- Saved-record query: <https://gis.toronto.ca/arcgis/rest/services/cot_geospatial2/FeatureServer/77/query?objectIds=2099%2C2088&outFields=*&returnGeometry=false&f=pjson>
- Downloaded: **November 18, 2026** (America/Toronto)
- Publisher: City of Toronto, `cot_geospatial2` ArcGIS FeatureServer

On the download date, layer 5 returned only two records, both permanent expressway-ramp closures; it had no lane-only record. To create the required full-closure/lane-restriction pair from current City JSON, the saved records came from layer 77, **RODARS Current Road Restriction Line**, in the same City FeatureServer. The saved feature attributes are unchanged from the JSON response; geometry was not requested.

The two cases are:

| Case | Street | Source description | V1 badge | Assessment |
| --- | --- | --- | --- | --- |
| Full closure (`OBJECTID 2099`) | Queen St E | “Full closure to vehicles…” | Road closed | Correct |
| Lane restriction (`OBJECTID 2088`) | Avenue Rd | “Northbound curb lane blocked…” | Road closed | Incorrect — known V1 behavior |

## Run locally

PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>. The page shows each street, its start and end dates, and the intentionally unconditional **Road closed** badge.

## Replay both cases

Run the focused replay:

```powershell
python scripts/replay_v1.py
```

Expected V1 result:

```text
PASS - full closure: 'Road closed' is correct
REPRODUCED - lane restriction: 'Road closed' is incorrect
```

Run the full test suite:

```powershell
python -m unittest -v
```

The tests assert the saved descriptions, displayed streets and dates, and the exact known mislabel. Do not “fix” the lane badge in V1; its failure is the incident baseline.
