# Australian Census Data

Builds the 2021 ABS geography urbanstats uses into `data/processed/`:

    pip install -r requirements.txt
    python3 build.py

| Layer | |
|---|---|
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
