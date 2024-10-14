from __future__ import annotations
import argparse
import time
import sys
from datetime import timedelta
from pathlib import Path

import PIL.ExifTags
import PIL.Image
import PIL.ImageOps


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("image_path", type=Path, help="Path to the base directory of all images")
parser.add_argument("--glob", dest="image_glob", default="**/*.jpg", help="A pathlib glob for image files under image_path")


def exif_aware_size_new(img_fn) -> tuple[int, int]:
    img = PIL.Image.open(img_fn)

    exif = img.getexif()

    orientation = exif.get(PIL.ExifTags.Base.Orientation, 1)

    if orientation in (1, 2, 3, 4):
        return (img.width, img.height)
    elif orientation in (5, 6, 7, 8):
        return (img.height, img.width)
    else:
        raise ValueError(f"Unknown EXIF orientation: {orientation}")


def exif_aware_size_old(img_fn) -> tuple[int, int]:
    img = PIL.Image.open(img_fn)
    # NOTE: exif_transpose() is an expensive operation, even with in_place=True
    PIL.ImageOps.exif_transpose(img, in_place=True)

    return (img.width, img.height)


def main():
    args = parser.parse_args()

    images = list(args.image_path.glob(args.image_glob))

    print(f"Determining width/height of {len(images)} images")

    old_acc = timedelta(seconds=0)
    new_acc = timedelta(seconds=0)

    for img_fn in images:
        start_old = time.monotonic()

        old_result = exif_aware_size_old(img_fn)

        stop_old = time.monotonic()
        dt_old = timedelta(seconds=stop_old - start_old)
        old_acc += dt_old


        start_new = time.monotonic()

        new_result = exif_aware_size_new(img_fn)

        stop_new = time.monotonic()
        dt_new = timedelta(seconds=stop_new - start_new)
        new_acc += dt_new


        assert new_result == old_result, "New way does not match old way"


    print(f"\tOld way took: {old_acc.total_seconds():.3e} sec")
    print(f"\tNew way took: {new_acc.total_seconds():.3e} sec")


if __name__ == "__main__":
    main()
