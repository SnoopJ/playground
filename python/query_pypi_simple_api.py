"""
Sample program showing communication with PyPI's Simple API (as described in
PEP 503 [1]) to list out available packages and available files for a given
package

Based on a question in #python on Libera.chat on 19 Oct 2022

[1] https://peps.python.org/pep-0503/
"""
from xml.etree import ElementTree

# third-party
import requests


INDEX_BASE_URL = "https://pypi.org"


def _islink(s: str) -> bool:
    # crude, but effective
    return s.strip().startswith("<a href=")


def _filter_links(doc: str):
    # unfortunately, the document PyPI returns isn't *quite* valid XML, but we drop the <meta> tag, ElementTree can handle it
    sanedoc = "\n".join(line for line in doc.splitlines() if "<meta" not in line)
    tree = ElementTree.fromstring(sanedoc)

    for tag in tree.iter(tag="a"):
        link_text = tag.text
        link_href = tag.attrib["href"]

        yield link_text, link_href


def available_packages():
    response = requests.get(INDEX_BASE_URL + "/simple")

    # turn HTTP errors into an exception
    response.raise_for_status()

    doc = response.content.decode()
    yield from _filter_links(doc)


def package_files(pkg: str):
    response = requests.get(INDEX_BASE_URL + "/simple/" + pkg)

    # turn HTTP errors into an exception
    response.raise_for_status()

    doc = response.content.decode()
    yield from _filter_links(doc)



print("---")
print("Listing out available packages")
print("---")
for count, (name, relurl) in enumerate(available_packages(), 1):
    print(f"[#{count}] file {name!r} is available at:\n  {INDEX_BASE_URL}{relurl}")

    if count >= 20:
        print("...and so on...\n")
        break

print("---")
print("Listing out available files for package 'numpy'")
print("---")
for count, (name, relurl) in enumerate(package_files("numpy")):
    print(f"[#{count}] file {name!r} is available at:\n  {INDEX_BASE_URL}{relurl}")

    if count >= 20:
        print("...and so on...\n")
        break
