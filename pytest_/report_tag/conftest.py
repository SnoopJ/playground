"""Here be dragons"""
import xml.etree.ElementTree as ET
import typing as t

import pytest
from _pytest.junitxml import xml_key, LogXML, _NodeReporter


def _node_adder(reporter: _NodeReporter):

    def _add_node(n: t.Union[ET.Element, str], **kwargs):
        safe_kwargs = {k: str(v) for k,v in kwargs.items()}
        if isinstance(n, str):
            node = ET.Element(n, **safe_kwargs)
        elif isinstance(n, ET.Element):
            if kwargs:
                raise ValueError("Keyword arguments cannot be given alongside an instance of xml.etree.ElementTree.Element")
            # element passes through with no modification
            node = n
        else:
            raise TypeError(f"node must be an instance of str or xml.etree.ElementTree.Element")

        reporter.append(node)

    return _add_node


@pytest.fixture
def record_tag(request):
    """
    Augment the JUnit output for the current test

    The fixture can be used in two ways:

    ### Simple tags
    ```
    record_tag("tagname", attr1=42, attr2=[1, 2, 3])
    ```

    producing the following output (note: attributes are run through `str()`):

    ```
    <tagname attr1="42", attr2="[1, 2, 3]" />
    ```

    ### Arbitrary contents
    ```
    record_tag(element)
    ```

    which appends the `ElementTree` instance `element` directly as a child of
    the current `<testcase>`
    """
    xml = request.config._store.get(xml_key, None)
    if not isinstance(xml, LogXML):
        raise TypeError("Can only add tags to instances of _pytest.junitxml.LogXML")

    def noop(elem):
        pass

    if xml is None:
        return noop

    node_reporter: _NodeReporter = xml.node_reporter(request.node.nodeid)
    return _node_adder(node_reporter)
