# Australian Census Data

Builds the 2021 ABS geography urbanstats uses into `data/processed/`:

    pip install -r requirements.txt
    python3 build.py

A failed download leaves a partial file in `data/raw/`; delete it and re-run.

| Layer | |
|---|---|
| MB | Mesh Block, the smallest unit; populated ones are written as points to `mb_blocks.npz` |
| SA1 | Statistical Area Level 1, the unit ABS publishes census tables for |
| STE | State or territory |
| SA2 | Statistical Area Level 2 |
| SUA | Significant Urban Area |
| UCL | Urban Centre and Locality |
| LGA | Local Government Area |
| SAL | Suburb and Locality |
| POA | Postal Area |
| CED | Commonwealth Electoral Division |
| SEDL | State Electoral Division, lower house |
| SEDU | State Electoral Division, upper house (Vic, WA, Tas only) |

SEDL and SEDU are not ABS layers: `abs/electorates.py` splits ABS's single SED layer into them.
