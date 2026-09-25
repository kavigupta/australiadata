import os
import re
import zipfile

import pandas as pd

SA1_CODE = "SA1_CODE_2021"
GCP_ZIP = "2021_GCP_SA1_for_AUS_short-header.zip"


def table_parts(archive, table):
    """Members of one GCP table; wide tables are split across A/B/C... parts."""
    pattern = re.compile(rf"2021Census_{table}[A-Z]?_AUST_SA1\.csv")
    names = sorted(n for n in archive.namelist() if pattern.fullmatch(os.path.basename(n)))
    assert names, f"no CSVs for {table} in {GCP_ZIP}"
    return names


def load_table(raw_dir, table):
    with zipfile.ZipFile(os.path.join(raw_dir, GCP_ZIP)) as archive:
        parts = [
            pd.read_csv(archive.open(name)).set_index(SA1_CODE)
            for name in table_parts(archive, table)
        ]
    joined = pd.concat(parts, axis=1)
    assert not joined.columns.duplicated().any(), f"{table}: duplicate columns across parts"
    return joined
