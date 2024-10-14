This example shows off two ways to retrieve the width/height of an image in a
way that respects [EXIF](https://en.wikipedia.org/wiki/Exif) metadata about
an image's orientation.

The 'old' way is much slower because it calls [`exif_transpose`](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html#PIL.ImageOps.exif_transpose)
and performs an expensive image transformation that isn't necessary if _only_
the width/height are needed. In the case that led me to write this code, I need
to know the image size to scale some image annotations (bounding boxes), but I
do not need the image data itself.

The 'new' way follows some of the prelude logic of `exif_transpose` but does
_not_ transform the image, only returns the width/height pair based on which
transformation _would_ be applied.

```
$ python3 fast_exifaware_size.py /path/to/my/images
Determining width/height of 199 images
        Old way took: 2.504e+01 sec
        New way took: 9.144e-02 sec
```
