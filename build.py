#!/usr/bin/env python3
import os

import numpy as np

from abs.blocks import build_blocks
from abs.electorates import split_sed, write_zipped_shapefile
from abs.regions import REGION_LAYERS, normalise
from download import RAW_DIR, download_all

OUT_DIR = "data/processed"

LATLON_SCALE = 1_000_000


def write_blocks(out_dir, blocks):
    assert blocks.Person.max() < np.iinfo(np.uint16).max
    assert blocks.Dwelling.max() < np.iinfo(np.uint16).max
    categories, category_codes = np.unique(blocks.MB_CATEGORY_NAME_2021.to_numpy().astype(str), return_inverse=True)
    assert len(categories) <= np.iinfo(np.uint8).max + 1
    np.savez_compressed(
        os.path.join(out_dir, "mb_blocks.npz"),
        mb_code=blocks.MB_CODE_2021.to_numpy().astype(np.int64),
        sa1_code=blocks.SA1_CODE_2021.to_numpy().astype(np.int64),
        population=blocks.Person.to_numpy().astype(np.uint16),
        dwellings=blocks.Dwelling.to_numpy().astype(np.uint16),
        lat=np.round(blocks.lat.to_numpy() * LATLON_SCALE).astype(np.int32),
        lon=np.round(blocks.lon.to_numpy() * LATLON_SCALE).astype(np.int32),
        categories=categories,
        category=category_codes.astype(np.uint8),
    )


def main():
    download_all()
    os.makedirs(OUT_DIR, exist_ok=True)

    lower, upper = split_sed(os.path.join(RAW_DIR, "SED_2021_AUST_GDA2020_SHP.zip"))
    regions = [("SEDL_2021_AUST", lower), ("SEDU_2021_AUST", upper)]
    regions += [
        (name, normalise(RAW_DIR, filename))
        for name, filename in REGION_LAYERS.items()
    ]
    for name, frame in regions:
        path = os.path.join(OUT_DIR, f"{name}_SHP.zip")
        write_zipped_shapefile(frame, path)
        print(f"  {name+'_SHP.zip':28} {len(frame):6,} regions  {os.path.getsize(path)/2**20:7.2f} MiB")

    blocks = build_blocks(
        os.path.join(RAW_DIR, "Mesh_Block_Counts_2021.xlsx"),
        os.path.join(RAW_DIR, "MB_2021_AUST_SHP_GDA2020.zip"),
    )
    write_blocks(OUT_DIR, blocks)
    path = os.path.join(OUT_DIR, "mb_blocks.npz")
    print(f"  {'mb_blocks.npz':28} {len(blocks):6,} blocks  {os.path.getsize(path)/2**20:7.2f} MiB")


if __name__ == "__main__":
    main()
