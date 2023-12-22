import argparse
import datetime
import re
import time
from dataclasses import dataclass
from pathlib import Path

import lxml.etree
import lxml.html
import requests
from feedgen.feed import FeedGenerator


# TODO: allow specifying alternate registers? or just scrape 'em all?

UTC_REGISTER_URL = "https://www.unicode.org/L2/L-curdoc.htm"
CACHE_LIFETIME_SEC = 24*60*60


parser = argparse.ArgumentParser(
    description="Scrape the HTML page for the UTC Documents Register and produce an RSS feed of the visible documents",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("--cache", default=True, action=argparse.BooleanOptionalAction, help="Cache the fetched HTML")
parser.add_argument("--cache-lifetime", type=int, default=24*60*60, help="Cache lifetime (in seconds)")
parser.add_argument("--outfile", default="UTC_register.xml")


@dataclass
class UTCDocument:
    id: str
    link: str
    title: str
    author: str
    date: datetime.date

    @property
    def dt(self):
        return datetime.datetime(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            tzinfo=datetime.timezone.utc
        )


def fetch_register(use_cache: bool, cache_lifetime: int) -> bytes:
    cache_pth = Path("UTC_register_current.htm")

    if use_cache and cache_pth.exists() and (time.time() - cache_pth.stat().st_mtime) <= cache_lifetime:
        print("Using cached register data")
        result = cache_pth.read_bytes()
    else:
        print("Fetching register data")
        response = requests.get(UTC_REGISTER_URL, allow_redirects=True)
        response.raise_for_status()
        if use_cache:
            cache_pth.write_bytes(response.content)

        result = response.content

    return result


def documents(register_html: bytes) -> list[dict]:
    doc_register = lxml.html.fromstring(register_html)
    # in English: find the *single* <table> that has a <tr><td> descendant that contains "Document Register"
    # will cause an exception if there is not exactly one matching node
    [doc_table] = doc_register.xpath("//table[./tr/td[contains(text(), 'Document Register')]]")

    # most of the rest of the table looks like:
    #
    #     <tr>
    #         <td nowrap><a href="L2023/23001-register-2022.htm">L2/23-001</a></td>
    #         <td>Complete UTC Document Register 2022</td>
    #         <td>Rick McGowan</td>
    #         <td nowrap>2023-01-05</td>
    #     </tr>
    #
    # with placeholder cells at the end:
    #
    #     <tr>
    #         <td nowrap><a href="L2023/NOTPOSTED">L2/23-286</a></td>
    #         <td>&nbsp;</td>
    #         <td>&nbsp;</td>
    #         <td nowrap>2023-12-</td>
    #     </tr>
    #

    documents = []

    for node in doc_table:
        if node.tag != "tr":
#             print(f"skipping non-row tag: <{node.tag}>")
            continue

        cells = node.getchildren()
        if not cells:
#             print(f"skipping empty row")
            continue 

        doc_ref, doc_title, doc_author, doc_date = cells
        if not doc_ref.getchildren() or b"NOTPOSTED" in lxml.etree.tostring(doc_ref):
#             print(f"skipping unpopulated row with doc_id: {lxml.etree.tostring(doc_id)!r}")
            continue

        doc_a = doc_ref.find("a")
        id = doc_a.text
        link = doc_a.attrib["href"]
        title = re.sub(r"\s+", " ", doc_title.text)
        author = doc_author.text
        date = datetime.date.fromisoformat(doc_date.text)

        documents.append(
            UTCDocument(
                id=id,
                link=link,
                title=title,
                author=author,
                date=date,
            )
        )

    return documents


def main():
    args = parser.parse_args()

    register_html = fetch_register(use_cache=args.cache, cache_lifetime=args.cache_lifetime)
    docs = documents(register_html)

    fg = FeedGenerator()
    fg.title("UTC Document Register")
    fg.link(href=UTC_REGISTER_URL)
    fg.description("UTC Document Register")

    for doc in docs:
        entry = fg.add_entry()
        entry.id(doc.id)
        entry.title(doc.title)
        entry.link(href=f"https://www.unicode.org/L2/{doc.link}")
        entry.author({"name": doc.author})
        entry.pubDate(doc.dt)


    fg.rss_file(args.outfile, pretty=True)
    print(f"RSS feed output written to {args.outfile}")


if __name__ == "__main__":
    main()
