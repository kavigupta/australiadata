import numpy as np
import pandas as pd
import geopandas as gpd

MB_SHEET_HEADER_ROW = 6


def load_mb_counts(counts_xlsx):
    book = pd.ExcelFile(counts_xlsx)
    parts = []
    for sheet in book.sheet_names:
        if not sheet.startswith("Table "):
            continue
        frame = pd.read_excel(book, sheet_name=sheet, skiprows=MB_SHEET_HEADER_ROW)
        if "MB_CODE_2021" not in frame.columns:
            continue
        parts.append(truncate_at_footnotes(frame))
    counts = pd.concat(parts, ignore_index=True)
    counts["MB_CODE_2021"] = counts.MB_CODE_2021.astype(np.int64)
    return counts


def truncate_at_footnotes(frame):
    """Each sheet ends with a blank row followed by ABS perturbation footnotes."""
    blank = frame.index[frame.MB_CODE_2021.isna()]
    end = blank[0] if len(blank) else len(frame)
    return frame.loc[: end - 1, ["MB_CODE_2021", "MB_CATEGORY_NAME_2021", "Dwelling", "Person"]]


def load_mb_points(mb_shapefile_zip):
    shapes = gpd.read_file(f"zip://{mb_shapefile_zip}").to_crs("epsg:4326")
    shapes = shapes[shapes.geometry.notna()]
    points = shapes.representative_point()
    return pd.DataFrame({
        "MB_CODE_2021": shapes["MB_CODE21"].astype(np.int64).values,
        "SA1_CODE_2021": shapes["SA1_CODE21"].astype(np.int64).values,
        "lon": points.x.values,
        "lat": points.y.values,
    })


# These have no boundary in the shapefile, so they get no representative point.
# NOUSUALRESIDENCE alone holds ~52k people, who are not placeable on a map.
UNPLACEABLE_CATEGORIES = ["NOUSUALRESIDENCE", "OFFSHORE", "MIGRATORY", "ANTARCTICA"]


def build_blocks(counts_xlsx, mb_shapefile_zip):
    counts = load_mb_counts(counts_xlsx)
    placeable = counts[~counts.MB_CATEGORY_NAME_2021.isin(UNPLACEABLE_CATEGORIES)]
    points = load_mb_points(mb_shapefile_zip)
    assert placeable.MB_CODE_2021.isin(set(points.MB_CODE_2021)).all(), \
        "placeable mesh block missing from shapefile"
    blocks = placeable.merge(points, on="MB_CODE_2021")
    return blocks[blocks.Person > 0].reset_index(drop=True)
