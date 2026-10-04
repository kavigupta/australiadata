#!/usr/bin/env python3
import os

from abs.electorates import split_sed, write_zipped_shapefile
from abs.regions import REGION_LAYERS, normalise
from download import RAW_DIR, download_all

OUT_DIR = "data/processed"


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


if __name__ == "__main__":
    main()
