#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from urllib.request import urlopen


BOUNDARIES = (
    "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs"
    "/edition-3-july-2021-june-2026/access-and-downloads/digital-boundary-files/"
)

BOUNDARY_FILES = (
    "MB_2021_AUST_SHP_GDA2020.zip",
    "SA1_2021_AUST_SHP_GDA2020.zip",
    "SA2_2021_AUST_SHP_GDA2020.zip",
    "SA3_2021_AUST_SHP_GDA2020.zip",
    "SA4_2021_AUST_SHP_GDA2020.zip",
    "GCCSA_2021_AUST_SHP_GDA2020.zip",
    "STE_2021_AUST_SHP_GDA2020.zip",
    "SUA_2021_AUST_GDA2020.zip",
    "UCL_2021_AUST_GDA2020_SHP.zip",
    "SOS_2021_AUST_GDA2020_SHP.zip",
    "LGA_2021_AUST_GDA2020_SHP.zip",
    "SAL_2021_AUST_GDA2020_SHP.zip",
    "POA_2021_AUST_GDA2020_SHP.zip",
    "CED_2021_AUST_GDA2020_SHP.zip",
    "SED_2021_AUST_GDA2020_SHP.zip",
)

FILES = {
    "Mesh_Block_Counts_2021.xlsx": "https://www.abs.gov.au/census/guide-census-data/mesh-block-counts/2021/Mesh%20Block%20Counts%2C%202021.xlsx",
    "2021_GCP_SA1_for_AUS_short-header.zip": "https://www.abs.gov.au/census/find-census-data/datapacks/download/2021_GCP_SA1_for_AUS_short-header.zip",
    **{name: BOUNDARIES + name for name in BOUNDARY_FILES},
}


def download(url: str, path: Path) -> None:
    if path.exists():
        print(f"exists: {path}")
        return

    print(f"downloading: {path.name}")
    with urlopen(url) as response, path.open("wb") as file:
        shutil.copyfileobj(response, file)


def download_all(out_dir: str) -> None:
    directory = Path(out_dir)
    directory.mkdir(parents=True, exist_ok=True)
    for filename, url in FILES.items():
        download(url, directory / filename)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download ABS Census data and boundaries.")
    parser.add_argument("--out-dir", default="data/raw", help="output directory")
    download_all(parser.parse_args().out_dir)


if __name__ == "__main__":
    main()
