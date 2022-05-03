# This sample is a refactoring exercise based on a question in Libera.chat #python on 2 May 2022
#
# User shared the following code, and asked for help getting it to work. Each line
# of the input is of the form `ID, X, Y`
#
# ```python
#    with arcpy.da.InsertCursor(os.path.join(outpath, newfc), ["SHAPE@"]) as cursor:
#        point = arcpy.Point()
#        array = arcpy.Array()
#        skipline = 0
#        for line in fileinput.input(textfile):
#            if skipline != 0:
#                point.ID, point.X, point.Y = line.split(",")
#                if point.ID not in fc_list:
#                    fc_list.append(point.ID)
#                else:
#                    pass
#
#                #works ---
#                if point.ID == 285797:
#                    array.add(point)
#                if point.ID == 286367:
#                    array.add(point)
#
#                #doesnt work ---
#                for item in fc_list:
#                    if point.ID == item:
#                        array.add(point)
#                    else:
#                        pass
#            else:
#                skipline += 1
#
#        polygon = arcpy.Polygon(array)
#        cursor.insertRow([polygon])
#    del cursor
# ```
#
# Below is my refactor of this code. If Point were more complicated to construct,
# I would perhaps write a helper of form `_parse_line(line: str) -> Point`, but
# the logic here was simple enough to only warrant two functions.
#
# This code does defer all insertions until the file has been fully parsed, but
# because the loading is done with a generator, you could get the old behavior of
# "as they're ready" with:
#

import fileinput
import os
from pathlib import Path
from pprint import pprint
from typing import Iterable, Generator

# arcpy appears to be from ArcGIS, so see arcpy.py for a set of stubs to demo the refactor without it
# for the real classes, see the ArcGIS documentation: 
#   https://pro.arcgis.com/en/pro-app/latest/arcpy/classes
import arcpy
from arcpy import Point, Array as PointArray, Polygon


HERE = Path(__file__).parent.resolve()


def _load_polygons(polygon_file: os.PathLike) -> Generator[Polygon, None, None]:
    """
    Extract polygons from the given filename

    Parameters
    ----------
    polygon_file
        Path to a CSV file with format:
            12345, 3.141592, 1.337
        Where the columns are, in order:
            - Unique ID of the curve being described
            - X value of the point
            - Y value of the point

    Notes
    -----
    I assume the points that make up an `Array` or `Polygon` are all adjacent to each other.
    If this were not the case, I would probably use a `dict[int, Array]` to accumulate `Point`s
    and then do a post-processing pass to turn the accumulated results into `Polygon`s.
    """
    filepth = Path(polygon_file)
    points = []
    for line in fileinput.input(filepth):
        pid, x, y = line.split(",")
        pid = int(pid)
        x = float(x)
        y = float(y)
        pt = Point(ID=pid, X=x, Y=y)
        if points and points[-1].ID != pt.ID:
            # if we have accumulated points and the ID changed, we're starting a new Polygon, so yield the old one first
            arr = PointArray(points)
            polygon = Polygon(arr)
            points = [pt]
            yield polygon
        else:
            # we're still building the next Polygon, accumulate this point
            points.append(pt)

    if points:
        arr = PointArray(points)
        polygon = Polygon(arr)
        yield polygon


textfile = HERE.joinpath("polygons.csv")
polygons = list(_load_polygons(textfile))

pprint(polygons)


# I can't demonstrate the cursor insertion code particularly well, but here's how I would spell it:

def insert_polygons(polygons: Iterable[Polygon]) -> None:
    with arcpy.da.InsertCursor(os.path.join(outpath, newfc), ["SHAPE@"]) as cursor:
        for pgon in polygons:
            cursor.insertRow([pgon])

# insert_polygons(polygons)
