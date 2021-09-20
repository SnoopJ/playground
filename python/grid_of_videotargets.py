"""
A doodle based on a question in Freenode #python on 12 Feb 2021 about
creating a data structure representing a grid of network-addressable
video display targets
"""

import attr
import csv
from dataclasses import dataclass
from ipaddress import IPv4Address

# first way, using attrs (see attrs.org)
@attr.s
class NetworkVideoTarget:
    """
    An object representing a network destination for a video we want to play
    """
    address = attr.ib(type=IPv4Address)
    video = attr.ib(type=str, default="placeholder.mp4")


# second way using stdlib dataclass, which is a tiny subset of attrs
# note: attrs can do this kind of annotation-driven thing, too, just replace @attr.s
# with @attr.s(auto_attribs=True)
@dataclass
class BoringNetworkVideoTarget:
    """
    *Also* an object representing a network destination for a video we want to play
    """
    address: IPv4Address
    video: str = "placeholder.mp4"


def make_grid(videos, cls=NetworkVideoTarget):
    # note: it could be ragged, this might be wrong! but I'm being lazy
    width = len(videos[0])

    base_address = int(IPv4Address("192.168.0.0"))  # arbitrary, we'll offset from here
    
    grid = dict()
    for nrow, row in enumerate(videos):
        for ncol, vid in enumerate(row):
            offset = width*nrow + ncol
            addr = IPv4Address(base_address + offset)  # note: built from an int!
            grid[nrow, ncol] = cls(address=addr, video=vid)

    return grid


# demo time!

from io import StringIO  # a buffer like what an open() would give us
from pprint import pprint  # pretty printer
import random

sample_csv = StringIO("""
doge.mp4, cade.webm
frogge.avi, capybara.oggv
""".strip())

if __name__ == "__main__":
    # in the real world, you'd do `with open(some_file, "r") as f: videos = list(csv.reader(f))`
    videos = [[fn.strip() for fn in row] for row in csv.reader(sample_csv)]
    print("videos:")
    pprint(videos)

    print("---")
    
    attrs_grid = make_grid(videos)
    print("attrs grid:")
    pprint(attrs_grid)

    print("---")

    x, y = (random.randint(0, 1) for _ in range(2))
    print(f"Indexing the point {x,y}:")
    instance = attrs_grid[x, y]
    print(instance.address)
    print(instance.video)

    print("---")

    dataclass_grid = make_grid(videos, cls=BoringNetworkVideoTarget)
    print("dataclass grid:")
    pprint(dataclass_grid)

    print("---")

    x, y = (random.randint(0, 1) for _ in range(2))
    print(f"Indexing the point {x,y}:")
    instance = dataclass_grid[x, y]
    print(instance.address)
    print(instance.video)

    print("---")

    for cls in (NetworkVideoTarget, BoringNetworkVideoTarget):
        instance = cls(IPv4Address("127.0.0.1"))
        print(f"{cls.__name__} created without specifying a video:\n\t{instance}")
