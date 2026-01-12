"""
This sample illustrates a solution to a problem I encountered while parsing
HTML served by Wiktionary.org (which is unfortunately more reliable than the
idiosyncratic JSON served up by their API[1])

The problem is that Wiktionary arranges its definitions such that the reliable
part-of-speech heading is a *sibling* to the definition it is associated with,
rather than a parent. My parser needs to select both of these so that I know
which part-of-speech goes with each definition, but identifying which <span>s
contain definitions depends on looking for that part of speech. A lightly
modified sample:

    <div><h4 id="Noun">Noun</h4></div>
    <figure><!-- ... --></figure>   <!-- NOTE: the <span> of interest is not necessarily the *next* sibling tag -->
    <p><span class="headword-line"><strong class="Latn headword" lang="en">pool</strong> (<i>plural</i> <b class="Latn form-of lang-en p-form-of" lang="en"><a href="/wiki/pools#English" title="pools">pools</a></b>)</span>
    </p>

The approach here allows us to select all such pairings of (<div>, <span>)
and present them in the order they appear in the document, which is important
to my downstream application

[1] https://en.wiktionary.org/wiki/User:Amgine/Wiktionary_data_%26_API#Wiktionary_API
"""
from itertools import batched  # Python 3.12+
from pprint import pprint

import lxml.html


# NOTE: in the Wiktionary use-case, this list is a large collection of known parts of speech, the resulting
# predicate formed form it is quite large
TARGET_IDS = ["target", "other_target"]
ID_PREDICATE = " or ".join(f'@id="{tid}"' for tid in TARGET_IDS)
# NOTE: we can grab the target <div> and its sibling <span> by constructing an
# expression using XPath's union operator '|'
# see: https://www.w3.org/TR/1999/REC-xpath-19991116/#node-sets
DEFN_XPATH = f".//h4[{ID_PREDICATE}]/.. | .//h4[{ID_PREDICATE}]/../following-sibling::span"
# NOTE: in the 'real' Wiktionary problem, the heading level is not reliable, so the XPath expression is even
# more complicated, but that detail has been elided here

DUMMY_DOC = """\
<html>
<body>
    <div><h4 id="target">Target #1</h4></div>
    <span>actual text target</span>
    <div><h4 id="other_target">Target #2</h4></div>
    <span>another text target</span>
</body>
</html>
"""


def definitions(doc: str) -> list[tuple[lxml.html.Element, lxml.html.Element]]:
    root = lxml.html.fromstring(DUMMY_DOC)
    tags = root.xpath(DEFN_XPATH)
    yield from batched(tags, 2)


if __name__ == "__main__":
    lst = list(definitions(DUMMY_DOC))
    pprint([(div.text_content(), span.text_content()) for div,span in lst])
