import os
import re
import tempfile
import zipfile

import geopandas as gpd

# ABS packs both chambers into one SED layer, differently per state. Victoria and
# WA name the Legislative Assembly district and put its Legislative Council region
# in parentheses. Tasmania instead publishes the *intersection* of its 5 House of
# Assembly divisions with its 15 Legislative Council divisions, so "Bass
# (Launceston)" is a sliver rather than a seat. Dissolving on the base name gives
# the lower house everywhere; dissolving on the parenthetical gives the upper house
# in the three states that have one.
#
# WA's six regions are the pre-2021 ones; WA has since moved to a single statewide
# Legislative Council electorate.

NON_ELECTORAL_STATES = ["Other Territories", "Outside Australia"]

LOWER_HOUSE_COUNTS = {
    "New South Wales": 93, "Victoria": 88, "Queensland": 93,
    "Western Australia": 59, "South Australia": 47, "Tasmania": 5,
    "Northern Territory": 25, "Australian Capital Territory": 5,
}
UPPER_HOUSE_COUNTS = {"Victoria": 8, "Western Australia": 6, "Tasmania": 15}


def split_name(name):
    match = re.match(r"^(.*?) \((.*)\)$", name)
    return match.groups() if match else (name, None)


def load_sed(sed_zip):
    data = gpd.read_file(f"zip://{sed_zip}").to_crs("epsg:4326")
    data = data[data.geometry.notna()]
    data = data[~data.STE_NAME21.isin(NON_ELECTORAL_STATES)]
    names = [split_name(n) for n in data.SED_NAME21]
    data["base"] = [n[0] for n in names]
    data["region"] = [n[1] for n in names]
    return data


def dissolve_to(data, column):
    dissolved = data[["STE_NAME21", column, "geometry"]].dissolve(
        by=["STE_NAME21", column]
    )
    dissolved = dissolved.reset_index()
    return dissolved.rename(columns={column: "SED_NAME21"})


def split_sed(sed_zip):
    data = load_sed(sed_zip)

    lower = dissolve_to(data, "base")
    upper = dissolve_to(data[data.region.notna()], "region")

    assert dict(lower.groupby("STE_NAME21").size()) == LOWER_HOUSE_COUNTS
    assert dict(upper.groupby("STE_NAME21").size()) == UPPER_HOUSE_COUNTS
    return lower, upper


def write_zipped_shapefile(frame, path):
    """Matches how ABS ships every other boundary layer, so loaders stay uniform."""
    stem = os.path.basename(path)[: -len(".zip")]
    with tempfile.TemporaryDirectory() as tmp:
        frame.to_file(os.path.join(tmp, stem + ".shp"))
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name in sorted(os.listdir(tmp)):
                archive.write(os.path.join(tmp, name), name)
