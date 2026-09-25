"""Normalise the ABS boundary layers we commit.

ABS ships GDA2020 with null-geometry rows for the unplaceable categories and ESRI
sidecar indexes. urbanstats works in EPSG:4326, so convert once here rather than in
every consumer, and drop what the committed copy does not need.
"""

import os

import geopandas as gpd

# Only the layers urbanstats registers as region types. SED is split by
# abs.electorates instead; MB and SA1 are build inputs; GCCSA, SA3, SA4 and SOS have
# no region type (GCCSA duplicates SUA, SOS is a classification rather than places).
REGION_LAYERS = {
    "STE_2021_AUST": "STE_2021_AUST_SHP_GDA2020.zip",
    "SA2_2021_AUST": "SA2_2021_AUST_SHP_GDA2020.zip",
    "SUA_2021_AUST": "SUA_2021_AUST_GDA2020.zip",
    "UCL_2021_AUST": "UCL_2021_AUST_GDA2020_SHP.zip",
    "LGA_2021_AUST": "LGA_2021_AUST_GDA2020_SHP.zip",
    "SAL_2021_AUST": "SAL_2021_AUST_GDA2020_SHP.zip",
    "POA_2021_AUST": "POA_2021_AUST_GDA2020_SHP.zip",
    "CED_2021_AUST": "CED_2021_AUST_GDA2020_SHP.zip",
}

DROPPED_COLUMNS = ["LOCI_URI21", "SHAPE_Leng", "SHAPE_Area", "CHG_FLAG21", "CHG_LBL21"]


def normalise(raw_dir, filename):
    frame = gpd.read_file(f"zip://{os.path.join(raw_dir, filename)}")
    frame = frame[frame.geometry.notna()].to_crs("epsg:4326")
    keep = [c for c in frame.columns if c not in DROPPED_COLUMNS]
    return frame[keep].reset_index(drop=True)
