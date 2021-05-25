"""
Sample showing how to modify the parsing behavior of the `json` library

Notes
-----
The JSON specification [1] does not require object keys to be unique.
Section 6 ("Objects") states:

    > The JSON syntax does not impose any restrictions on the strings used as
    > names, does not require that name strings be unique, and does not assign
    > any significance to the ordering of name/value pairs. These are all
    > semantic considerations that may be defined by JSON processors or in
    > specifications defining specific uses of JSON for data interchange.

In other words, if a JSON object has a repeated key, there is no defined
"correct" behavior when parsing it! A parser may do whatever it wants.

IETF RFC 7159 [2] extends ECMA-404 to suggest that "names within an object
SHOULD be unique," partially constraining at least the behavior of systems that
emit JSON, but the parsing ambiguity still exists among systems that implement
that standard.

When presented with duplicate keys, the Python stdlib module `json` [3] will by
default decode using the last given value of a key, which matches the behavior
of `dict()` when passed an iterable of key-value pairs. However, the module's
behavior is very customizable, so we can reach into the parsing process to
rectify this and define our own behavior, or even define our own subclass of
`json.JSONDecoder`.

In this sample, I show a simpler technique using the `object_pairs_hook`

References
----------
[1] ECMA-404 https://www.ecma-international.org/wp-content/uploads/ECMA-404_2nd_edition_december_2017.pdf
[2] https://datatracker.ietf.org/doc/html/rfc7159.html#section-4
[3] https://docs.python.org/3/library/json.html
"""
import json

# this is a valid JSON document, but it contains the key "data" twice!
doc = """
{
    "data": [1, 2, 3],
    "data": [4, 5, 6]
}
"""

def hook(pairs):
    newpairs = {}
    for k,v in pairs:
        if isinstance(v, list):
            lst = newpairs.setdefault(k, [])  # get existing value, or initialize with []
            lst.extend(v)  # add the current values
    return newpairs

naive_parse = json.loads(doc)
extended_parse = json.loads(doc, object_pairs_hook=hook)

print("document:")
print(doc)

print("naive_parse:")
print(naive_parse)  # {'data': [4, 5, 6]}

print("extended_parse:")
print(extended_parse)  #  {'data': [1, 2, 3, 4, 5, 6]}
