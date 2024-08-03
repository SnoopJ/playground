"""
Script to copy .fit files from a Garmin device at a fixed path (`GARMIN_ROOT`)
to the same location as this script, and create a map of the GPS tracks
contained therein overlaid on map tiles from OpenStreetMap
"""
import itertools
import math
import shutil
from pathlib import Path

import numpy as np
import PIL.Image
import requests
from garmin_fit_sdk import Stream, Decoder
from matplotlib import pyplot as plt


HERE = Path(__file__).parent
GARMIN_ROOT = Path("/path/to/GARMIN/Garmin")  # TODO: replace with the path to your mount point


def copy_fit_files():
    for subdir in ("Activity", "Monitor"):
        HERE.joinpath(subdir).mkdir(exist_ok=True)

        for pth in GARMIN_ROOT.joinpath(subdir).glob("*.fit"):
            if HERE.joinpath(pth.name).exists():
                continue
            print(f"Copying FIT file: {str(pth)!r}")
            shutil.copy(pth, HERE.joinpath(subdir))


def latlon_from_fit(infn: Path, fits_archive) -> np.ndarray:
    assert infn.exists(), f"File does not exist: {str(infn)!r}"

    strm = Stream.from_file(infn)
    dec = Decoder(strm)
    messages, errors = dec.read()

    # Garmin stores coordinates in units of "semicircles"
    # https://www.gps-forums.com/threads/explanation-sought-concerning-gps-semicircles.1072/
    SEMICIRCLES_TO_DEG = 180 / (2**31)

    coords = [(rec["position_lat"], rec["position_long"]) for rec in messages["record_mesgs"] if "position_lat" in rec]
    latlon = SEMICIRCLES_TO_DEG * np.asarray(coords)
    return latlon


TILE_SIZE = 256


def point_to_pixels(lon, lat, zoom):
    """convert gps coordinates to web mercator"""
    r = math.pow(2, zoom) * TILE_SIZE
    lat = math.radians(lat)

    x = int((lon + 180.0) / 360.0 * r)
    y = int((1.0 - math.log(math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * r)

    return x, y


# OSM integration code courtesy of: https://bryanbrattlof.com/adding-openstreetmaps-to-matplotlib/
OSM_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format

# It's polite to let OSM know who we are
USER_AGENT = os.environ.get("USER", "UnknownUser") + "-Garmin-Script"

def osm_tile(x_tile, y_tile, zoom) -> PIL.Image.Image:
    pth = Path(HERE, f"{x_tile}_{y_tile}_{zoom}.png")
    if pth.exists():
        print("Using cached tile image")
        img = PIL.Image.open(pth)
    else:
        print("Retrieving tile from OSM")
        with requests.get(OSM_TILE_URL(x=x_tile, y=y_tile, z=zoom), headers={"User-Agent": USER_AGENT}) as resp:
            resp.raise_for_status() # just in case
            pth.write_bytes(resp.content)
            img = PIL.Image.open(pth)

    return img


def osm_img(x0_tile, y0_tile, x1_tile, y1_tile, zoom) -> PIL.Image.Image:
    # full size image we'll add tiles to
    img = PIL.Image.new('RGB', [
        (x1_tile - x0_tile) * TILE_SIZE,
        (y1_tile - y0_tile) * TILE_SIZE,
    ])

    # loop through every tile inside our bounded box
    for x_tile, y_tile in itertools.product(range(x0_tile, x1_tile), range(y0_tile, y1_tile)):
        tile_img = osm_tile(x_tile, y_tile, zoom)
        box_x = (x_tile - x0_tile) * TILE_SIZE
        box_y = (y_tile - y0_tile) * TILE_SIZE
        # add each tile to the full size image
        img.paste(
            im=tile_img,
            box=(box_x, box_y),
        )

    return img


def plot(fits_files, osm: bool = True):
    plt.figure(figsize=(18, 12))

    lonlim = [math.inf, -math.inf]
    latlim = [math.inf, -math.inf]

    FITS_ARCHIVE = Path(HERE, "fits.npz")
    if FITS_ARCHIVE.exists():
        fits = dict(np.load(FITS_ARCHIVE))
    else:
        fits = {}

    for fn in fits_files:
        infn = Path(fn)
        if infn.name in fits:
            print(f"Using cached lat/lon data for {fn!r}")
            latlon = fits[infn.name]
            print(latlon.mean())
        else:
            print(f"Loading data for {fn!r} from FIT file")
            latlon = latlon_from_fit(infn, fits)
            fits[infn.name] = latlon

        lat, lon = np.split(latlon, 2, axis=-1)

        lonlim[0] = min(lonlim[0], np.nanmin(lon))
        lonlim[1] = max(lonlim[1], np.nanmax(lon))
        latlim[0] = min(latlim[0], np.nanmin(lat))
        latlim[1] = max(latlim[1], np.nanmax(lat))

        # NOTE: Sometimes an activity is recorded, paused, and then resumed from a location far away geographically from
        # the pause location. Drawing this naively produces ugly interpolation between the two. These lines insert a NaN
        # whenever the distance between two subsequent track points exceeds a threshold, which is a matplotlib trick to
        # prevent that interpolation. It is technically dropped one recorded point from the track, but in practice this
        # is not a very big deal.
        latdiff = np.ediff1d(lat)
        londiff = np.ediff1d(lon)
        idx = np.argwhere((latdiff**2 + londiff**2)**0.5 > 0.001)
        lat[idx] = np.nan
        lon[idx] = np.nan

        # NOTE: You might prefer a different plotting style here, adjust to your personal taste
        plt.plot(lon, lat, 'b-', alpha=0.7, linewidth=4)

    np.savez(FITS_ARCHIVE, **fits)

    if osm:
        ZOOM = 13
        x0, y0 = point_to_pixels(lonlim[0], latlim[1], zoom=ZOOM)
        x1, y1 = point_to_pixels(lonlim[1], latlim[0], zoom=ZOOM)

        x0_tile, y0_tile = int(x0 / TILE_SIZE), int(y0 / TILE_SIZE)
        x1_tile, y1_tile = math.ceil(x1 / TILE_SIZE), math.ceil(y1 / TILE_SIZE)

        assert (x1_tile - x0_tile) * (y1_tile - y0_tile) < 50, "That's too many tiles!"

        img = osm_img(x0_tile, y0_tile, x1_tile, y1_tile, zoom=ZOOM)
        x, y = x0_tile * TILE_SIZE, y0_tile * TILE_SIZE
        img = img.crop((
            abs(int(x - x0)),  # left
            abs(int(y - y0)),  # top
            abs(int(x - x1)),  # right
            abs(int(y - y1)),  # bottom
        ))

        plt.imshow(img, extent=(lonlim[0], lonlim[1], latlim[0], latlim[1]))

    plt.xlabel('longitude')
    plt.ylabel('latitude')

    outfn = HERE.joinpath("out.png")
    plt.savefig(outfn)
    print(f"GPS track plotted to {outfn!r}")


if __name__ == "__main__":
    copy_fit_files()
    all_files = list(HERE.joinpath("Activity").glob("*.fit"))
    plot(all_files)
