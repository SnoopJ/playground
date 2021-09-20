import xml.etree.ElementTree as ET

import pytest


def test_foo_baseline(record_property):
    record_property("this is what", "junit can do")
    record_property("but it's kinda", "limited, especially")
    record_property("when storing structred data like", {"foo": 42})
    ...


@pytest.mark.parametrize("foo", [1,2,3])
def test_foo_augmented(foo, record_tag):
    record_tag("custom_tag_empty")
    record_tag("custom_tag_with_data", foo=42, bar=-1, baz="O frabjous day!")


def complex_subtree():
    tree = ET.Element("custom_tag_tree")
    a = ET.SubElement(tree, "a", bar=str(-1))
    b = ET.SubElement(a, "b")
    c = ET.SubElement(b, "c", someattrib="someval")
    d = ET.SubElement(b, "d")
    for N in range(10):
        ET.SubElement(d, "item", num=str(N), running_sum=str(sum(range(N+1))))
    e = ET.SubElement(d, "comment", depth="pretty deep, right?")

    return tree


def test_foo_augmented_by_element(record_tag):
   record_tag("custom_tag_empty")
   record_tag(ET.Element("custom_tag_via_ElementTree", foo=str(42)))

   tree = complex_subtree()
   record_tag(tree)
