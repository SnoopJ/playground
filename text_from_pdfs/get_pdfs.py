"""
Download well report PDFs from the state of Texas website according to a list
of IDs given in an auxiliary file.
"""

import requests
import time

try:
    from tqdm import tqdm
except ImportError:
    print("tqdm is not installed, proceeding without fancy progress bar :'(")
    def tqdm(it, desc: str="", *args, **kwargs):
        if desc:
            print(desc)
        return iter(it)

REQUEST_DT = 50e-3  # minimum time (sec) between subsequent requests
URL_TEMPLATE = r"https://www3.twdb.texas.gov/apps/waterdatainteractive/GetReports.aspx?Num={well_id}&Type=SDR-Well"

def get_pdf(well: int) -> bytes:
    url = URL_TEMPLATE.format(well_id=str(well))
    return requests.get(url).content

if __name__ == "__main__":
    with open("well_ids.txt", "r") as infile:
        well_ids = [int(line) for line in tqdm(infile, desc="Reading well IDs") if line]

    for wid in tqdm(well_ids, desc="Downloading PDFs"):
        with open(f"{wid}.pdf", "wb") as outfile:
            outfile.write(get_pdf(wid))
            time.sleep(REQUEST_DT)


