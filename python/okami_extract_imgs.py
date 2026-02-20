"""
Given Ōkami HD game files as decrypted by `okami-encdec`, scan through
the given file and try to extract the embedded DDS images as PNGs

NOTE: I wrote this to handle the `Illust*.dat` files in `data_pc/etc/gallery`,
it is likely to fail for other files
"""
import sys
from io import BytesIO
from pathlib import Path

# third-party, provided by: pip install Pillow
import PIL.Image

CHUNK_SIZE = 8192

def dds_data(fn):
    acc = b""
    with open(fn, "rb") as f:
        while buf := f.read(CHUNK_SIZE):
            try:
                idx = buf.index(b"DDS ")
                acc += buf[:idx]
                if acc:
                    yield acc
                acc = buf[idx:]
            except ValueError:
                acc += buf

        if acc:
            yield acc


if __name__ == "__main__":
    target_fn = Path(sys.argv[1])

    outdir = Path(f"{target_fn.stem}_out")
    outdir.mkdir(exist_ok=True)

    for num, data in enumerate(dds_data(target_fn)):
        dst = outdir.joinpath(f"{num}.png")
        if dst.exists():
            print(f"File exists, skipping: {dst}")
            continue
        try:
            img = PIL.Image.open(BytesIO(data))
            print(f"Writing {dst}")
            img.save(dst)
        except Exception as exc:
            dst2 = outdir.joinpath(f"{num}.dds")
            print(f"Could not write .png, writing {dst2}")
            dst2.write_bytes(data)
