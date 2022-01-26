from logging import getLogger, StreamHandler, Formatter
import sys

fmt_leaf = Formatter("LEAF: %(message)s")
hout_leaf = StreamHandler(sys.stdout)
hout_leaf.setFormatter(fmt_leaf)

fmt_root = Formatter("ROOT: %(message)s")
hout_root = StreamHandler(sys.stdout)
hout_root.setFormatter(fmt_root)

herr = StreamHandler(sys.stderr)

root = getLogger(__name__)
leaf1 = getLogger(__name__ + ".leaf1")
leaf2 = getLogger(__name__ + ".leaf2")

# N.B. leaf2 does NOT have any handlers!
leaf1.addHandler(hout_leaf)
root.addHandler(hout_root)

root.error("This is an error directly on the root logger")
leaf1.error("This is an error directly on leaf1 (which will propagate to the root handler and show up twice)")
leaf2.error("This is an error directly on leaf2 (which will propagate to the root handler and show up once)")

