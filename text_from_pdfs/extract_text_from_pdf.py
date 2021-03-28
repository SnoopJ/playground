"""
Extract information about well screens from PDFs downloaded from the state of
Texas database (see `get_pdfs.py`) and save them to `results.csv`

Note: this program in its current form will also extract casement information,
but it produces data clean enough to be finalized by light human editing
"""

import csv
import re
from pathlib import Path

import PyPDF2

try:
    from tqdm import tqdm
except ImportError:
    print("tqdm is not installed, proceeding without fancy progress bar :'(")
    def tqdm(it, desc: str="", *args, **kwargs):
        if desc:
            print(desc)
        return iter(it)


def get_page_text(pdf: PyPDF2.PdfFileReader, idx: int):
    return pdf.getPage(idx).extractText()


def get_all_text(pdf: PyPDF2.PdfFileReader):
    return "\n".join(get_page_text(pdf, idx) for idx in range(pdf.getNumPages()))


def maybe_extract_depths(lines: list) -> list:
    """
    Try to extract depths from the given a set of lines

    This function is written conservatively, only returning depth information
    for cases it's reasonably sure about, e.g.
        XXX to YYY
        XXX-YYY
        XXX' to YYY'
        XXX' -  YYY'
        XXX ft. to YYY ft.
        XXX ft. - YYY ft.

    Returns
    -------
    start: str
    stop: str
        If not found, "N/A"
    line: str
        The complete original line
    """
    UNIT = r"(?:'|ft\.?)"
    DGTS = r"(\+?\d+)"
    SEP = r"(?:-|to)"
    DIGITS_PATTERN = rf"{DGTS}\s*{UNIT}?\s*{SEP}\s*{DGTS}\s*{UNIT}?"
    for line in lines:
        m: list = re.findall(DIGITS_PATTERN, line)
        if not m:
            start = "N/A"
            stop = "N/A"
        else:
            start, stop = m[0]
            if start.startswith("+"):
                start = start.replace("+", "-")

        yield start, stop, line


def get_setting_info(fn: Path) -> list:
    """Load the PDF at the given path and try to extract the setting information from that report"""
    pdffile = PyPDF2.PdfFileReader(fn.open('rb'))

    txt = get_all_text(pdffile)
    lines = txt.splitlines()

    try:
        setidx = next(num for num,line in enumerate(lines) if "Setting From/To" in line)
    except StopIteration as exc:
        raise ValueError(f'Cannot find the "Setting From/To" table in {fn}') from exc

    if lines[setidx+1] == "No Data":
        print(f"Explicitly no data for {fn}")
        endidx = setidx + 2
    else:
        gen = (num for num,line in enumerate(lines) if "Certification Data" in line)
        endidx = next(gen)

    if endidx < setidx:
        raise ValueError(f"Certification section before Setting section in file {fn}")

    candidates = lines[setidx+1:endidx]

    return [(fn.stem, *fields) for fields in maybe_extract_depths(candidates)]


if __name__ == "__main__":
    print("Searching for .pdf files in current directory")
    MAX_FILES = None  # set to an integer to limit the number of files processed
    currdir = Path()
    fns = list(currdir.glob("*.pdf"))
    fns = fns[:MAX_FILES]
    print(f"Found {len(fns)} files")

    # go through the files and process each one, collecting the results
    results = []
    for fn in tqdm(fns, desc="Extracting settings from PDFs"):  # if tqdm is not installed this line is basically `for fn in fns:`
        try:
            res = get_setting_info(fn)
            results.extend(res)
        except Exception as exc:
            print(f"Failed to extract from {fn}, exception was: {repr(exc)}")
            print("Continuing...")

    # order the results by: 1) whether or not we extracted data (N/A first)
    #                       2) well ID, ascending
    #                       3) depth, if we have one
    def _order(row):
        wellid, start, stop, *rest = row
        isNA = -1 if start == "N/A" else 1
        return (isNA, wellid, start)

    results = sorted(results, key=_order)

    # save the output
    with open("results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(results)
