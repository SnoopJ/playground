"""
A little script for selecting a random Zoom virtual background

If you want to use this for yourself:

    1) Add some custom virtual background to Zoom (doesn't matter what it is)
    2) Edit `TARGET_FILE` below to match the location of the copy of this image
       that Zoom made
    3) Edit `CANDIDATE_BG_PATHS` below to match the location(s) of the images
       you want to select from
    4) Run this program any time you want to rotate your background. I plan to
       put mine into a system service

The idea here is that Zoom always looks at this file for 'that' background, so
if we swap the original file for some other image, our background is different.
"""
from pathlib import Path
import os
import os.path
import random
import shutil
import subprocess


HERE = Path(__file__).parent.resolve()

# As far as I can tell, Zoom's user settings are stored in an encrypted SQLite DB,
# so the easiest thing to do is to set the virtual background once by hand, then
# replace the associated file with a symlink that we can rotate. This requires
# either changing the virtual background away and back in the UI, or restarting the
# Zoom client.
TARGET_FILE = Path(os.path.expanduser("~/.zoom/data/VirtualBkgnd_Custom/{0b9a4beb-31c8-46cd-aae5-a07e025e59a7}"))


CANDIDATE_BG_PATHS = [
    HERE.joinpath("misc"),
]
def _candidate_bgs():
    for pth in CANDIDATE_BG_PATHS:
        yield from pth.glob("*.jpg")
        yield from pth.glob("*.jpeg")
        yield from pth.glob("*.png")


if __name__ == "__main__":
    candidates = list(_candidate_bgs())
    assert candidates, f"No images found in {CANDIDATE_BG_PATHS=}"

    newimg = random.choice(candidates)

    TARGET_FILE.unlink(missing_ok=True)
    shutil.copyfile(newimg, TARGET_FILE)
    print("New virtual background installed")

    # Zoom won't pick up the change unless we change our background away and
    # back in the UI or restart; a restart is simpler
    subprocess.run(["killall", "zoom"])
    print("Starting Zoom…")
    subprocess.Popen(["zoom"])
