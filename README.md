# Australian Census Data

Downloads the 2021 Australian Census (ABS) and builds the geography urbanstats
consumes. The census tables are collapsed in urbanstats, not here.

## Build

    python3 build.py

Downloads ~1.2 GB into `data/raw/` and writes `data/processed/`. Skips files
already downloaded; `--skip-download` skips that step entirely. Needs
geopandas; the `urbanstats-310` env has it.

Nothing under `data/` is committed — build it where you need it.

`download.py` runs standalone if you only want the raw data. It is stdlib only and
exists to document where each file came from, so it is deliberately not robust — a
failed download leaves a partial file, so delete it and re-run.

## Output

- Boundary layers as zipped shapefiles, EPSG:4326, with null geometries and ESRI
  sidecars dropped (`abs/regions.py`): STE, SA2, SUA, UCL, LGA, SAL, POA, CED,
  SEDL, SEDU.

ABS ships both chambers as one `SED` layer, so `abs/electorates.py` splits it into
`SEDL` and `SEDU`. `MB` and `SA1` are build inputs, not display regions.
