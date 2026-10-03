#!/usr/bin/env python3
"""Download the ABS census release and build the geography urbanstats consumes.

The census tables themselves are collapsed in urbanstats, so the cell mapping lives
next to the statistics it defines.
"""

import argparse
import os

from abs.electorates import split_sed, write_zipped_shapefile
from abs.regions import REGION_LAYERS, normalise
from download import download_all


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--out-dir", default="data/processed")
    args = parser.parse_args()

    if not args.skip_download:
        download_all(args.raw_dir)
    os.makedirs(args.out_dir, exist_ok=True)

    lower, upper = split_sed(os.path.join(args.raw_dir, "SED_2021_AUST_GDA2020_SHP.zip"))
    regions = [("SEDL_2021_AUST", lower), ("SEDU_2021_AUST", upper)]
    regions += [
        (name, normalise(args.raw_dir, filename))
        for name, filename in REGION_LAYERS.items()
    ]
    for name, frame in regions:
        path = os.path.join(args.out_dir, f"{name}_SHP.zip")
        write_zipped_shapefile(frame, path)
        print(f"  {name+'_SHP.zip':28} {len(frame):6,} regions  {os.path.getsize(path)/2**20:7.2f} MiB")


if __name__ == "__main__":
    main()
