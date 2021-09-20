# report_tag
## a pytest fixture for adding arbitrary XML to JUnit output

### Example usage

Use the `record_tag` fixture in your tests

```python
import xml.etree.ElementTree as ET

def test_foo(record_tag):
    record_tag("custom_tag_empty")
    record_tag("custom_tag_with_data", foo=42, bar=-1, baz="O frabjous day!")

    tree = ET.Element("custom_tag_tree")
    a = ET.SubElement(tree, "a", bar=str(-1))
    record_tag(custom_tag_tree)
```

And the JUnit output will have the corresponding extra data:

```xml
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
  <testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1" time="0.119" timestamp="2021-07-02T21:46:36.499265" hostname="denton">
    <testcase classname="test_doc" name="test_foo" time="0.003">
      <custom_tag_empty/>
      <custom_tag_with_data foo="42" bar="-1" baz="O frabjous day!"/>
      <custom_tag_tree>
        <a bar="-1"/>
      </custom_tag_tree>
    </testcase>
  </testsuite>
</testsuites>
```
