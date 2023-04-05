# TODO:
#   * can the shift() arithmetic be delegated to move_to() and next_to() ?

import unicodedata
from typing import List

import icu  # https://pypi.org/project/PyICU/
from manim import *

# config["pixel_width"] = 800
config["pixel_height"] *= 2
config["frame_height"] *= 1
config["frame_width"] = 32


EDGE = "#006020"
FILL = "#cccccc"


W=0.85
H=0.8
DW=0.1
DH=0.1

def draw_codepoints(txt) -> VGroup:
    grp = VGroup()
    for idx, codept in enumerate(txt):
        DX = 0
        DY = idx*(H + DH)
        poly = (
            Rectangle(
                width=W,
                height=H,
                color=EDGE,
                fill_color=FILL,
                fill_opacity=1.0,
            )
            .shift(DOWN*DY)
            .shift(RIGHT*DX)
        )

        codept_txt = (
            Text(
                codept,
                color=BLACK,
                font_size=26,
            )
            .move_to(poly.get_center())
            .shift(DOWN*0.1)
        )

        if codept != " " and not len(codept_txt):
            codept_txt = (
                Text(
                    "\N{REPLACEMENT CHARACTER}",
                    color=BLACK,
                    font_size=32,
                )
                .move_to(poly.get_center())
                .shift(DOWN*0.1)
            )

        codept_label = (
            Text(
                f"U+{ord(codept):0>4x}",
                color=BLACK,
                font_size=12,
                font="sans-serif",
            )
            .move_to(poly.get_center())
            .shift(UP*0.25)
        )
        codept_name = (
            Text(
                unicodedata.name(codept, "???"),
                color=WHITE,
                font_size=28,
                font="sans-serif",
            )
            .next_to(poly, direction=RIGHT)
        )
        codept_info = VGroup(
            poly,
            codept_txt,
            codept_label,
            codept_name,
        )
        grp.add(codept_info)

    return grp


def graphemes(txt: str) -> List[str]:
    """Partition a string into a list of graheme clusters"""
    iter_grapheme = icu.BreakIterator.createCharacterInstance(icu.Locale.getUS())
    s = icu.UnicodeString(txt)
    iter_grapheme.setText(s)
    breaks = [0, *iter_grapheme]

    graphs = []
    for start, end in zip(breaks, breaks[1:]):
        graphs.append(txt[start:end])

    return graphs


def draw_grapheme_clusters(txt) -> VGroup:
    offset = 0
    grp = VGroup()
    for cluster in graphemes(txt):
        cluster_size = len(cluster)

        DX = 0
        DY = offset*(H + DH) + (H/2*cluster_size if cluster_size>1 else 0)

        GH = (H + DH)*cluster_size

        cluster_poly = (
            Rectangle(
                width=W + 0.2,
                height=GH,
                color=RED,
                fill_opacity=0.0,
            )
            .shift(DOWN*DY)
        )
        cluster_txt = (
            Text(
                cluster,
                color=RED,
                font_size=24,
            )
            .next_to(cluster_poly, direction=LEFT)
            .shift(DOWN*0.1)
        )
        grp.add(cluster_poly, cluster_txt)

        offset += cluster_size

    return grp


class UnicodeStrings(str, Enum):
    hello = "hello world"
    cava = "Ça va"
    cccava = "ÇÇÇa va"
    konbanwa = "こんばんは, 元気だ？"
    hankaku = "ﾊﾝｶｸｶﾀｶﾅ"
    tabkey = "\t⃣"
    zalgo = "f̶̲̔"


class MyScene(Scene):
    X0 = -2.5
    Y0 = -4.5

    def construct(self):

        grid = VGroup()
        # for txt in [UnicodeStrings.zalgo]:
        for txt in UnicodeStrings:

            grp = VGroup()

            codept_grp = draw_codepoints(txt)
            clusters_grp = draw_grapheme_clusters(txt)

            codept_grp.shift(RIGHT*self.X0).shift(DOWN*self.Y0)
            clusters_grp.shift(RIGHT*self.X0).shift(DOWN*self.Y0)

            grp.add(codept_grp, clusters_grp)
            grid.add(grp)

        # grid arrangement
        BUFF = 1.5
        NROW = 3
        NCOL = 3
        ROWALIGN = "u"*NROW
        CELLALIGN = "l"*NCOL
        grid.arrange_in_grid(rows=NROW , cols=NCOL, buff=BUFF, cell_alignments=CELLALIGN, row_alignments=ROWALIGN)

        # all done
        self.add(grid)
