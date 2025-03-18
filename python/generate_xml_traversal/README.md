## What

This sample shows off a solution to the minor problem of translating a file tree to the corresponding [WiX Toolset] XML.

[WiX Toolset]: https://wixtoolset.org/

## But… why?

I need to do this because WiX v5 does not seem capable of collecting a tree of this kind under a single `<Component>`,
which matters quite a lot for applications with lots of files in it (mine has 31k). There is somewhat of a superstition
in the Windows Installer community that files and components should always be 1:1, and while this does provide very nice
"database" presentation of an application, it can _drastically_ slow down install/uninstall times for large numbers of
small components. Your installer log files will be 100 MB+, etc. It's not a fun time.

As loathe as I am to statefully generate XML, this is a pretty okay solution to the problem I have in front of me as I
write up this example.

## Show me

```
$ python3 make_path_tree.py
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c1
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c2
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c2/d2c0.txt
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c1/d2c0
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c1/d2c0/d3c0
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c1/d2c0/d3c1.txt
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c1/d2c0/d3c0/d4c0.txt
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c1/d2c0/d3c0/d4c1.txt
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c0
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c1.txt
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c2.txt
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c0.txt
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c1
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c1/d4c0
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c1/d4c1.txt
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c1/d4c0/d5c0
Creating dir:  /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c1/d4c0/d5c0/d6c0
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c1/d4c0/d5c0/d6c0/d7c0.txt
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c1/d4c0/d5c0/d6c0/d7c1.txt
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c3/d3c1/d4c0/d5c0/d6c0/d7c2.txt
Creating file: /home/jgerity/personal/playground/python/generate_xml_traversal/tree/d0c0/d1c0/d2c0/d3c0.txt

$ python3 generate_wix_xml.py
Traversing tree/
<!-- BEGIN generated XML -->
<Directory Name="d0c0">
    <Directory Name="d1c0">
        <File Source="!(bindpath.bundle_root)\d0c0\d1c0\d2c1.txt" />
        <File Source="!(bindpath.bundle_root)\d0c0\d1c0\d2c2.txt" />
        <Directory Name="d2c0">
            <File Source="!(bindpath.bundle_root)\d0c0\d1c0\d2c0\d3c0.txt" />
        </Directory>
        <Directory Name="d2c3">
            <File Source="!(bindpath.bundle_root)\d0c0\d1c0\d2c3\d3c0.txt" />
            <Directory Name="d3c1">
                <File Source="!(bindpath.bundle_root)\d0c0\d1c0\d2c3\d3c1\d4c1.txt" />
                <Directory Name="d4c0">
                    <Directory Name="d5c0">
                        <Directory Name="d6c0">
                            <File Source="!(bindpath.bundle_root)\d0c0\d1c0\d2c3\d3c1\d4c0\d5c0\d6c0\d7c0.txt" />
                            <File Source="!(bindpath.bundle_root)\d0c0\d1c0\d2c3\d3c1\d4c0\d5c0\d6c0\d7c2.txt" />
                            <File Source="!(bindpath.bundle_root)\d0c0\d1c0\d2c3\d3c1\d4c0\d5c0\d6c0\d7c1.txt" />
                        </Directory>
                    </Directory>
                </Directory>
            </Directory>
        </Directory>
    </Directory>
    <Directory Name="d1c1">
        <Directory Name="d2c0">
            <Directory Name="d3c0">
                <File Source="!(bindpath.bundle_root)\d0c0\d1c1\d2c0\d3c0\d4c0.txt" />
                <File Source="!(bindpath.bundle_root)\d0c0\d1c1\d2c0\d3c0\d4c1.txt" />
            </Directory>
            <File Source="!(bindpath.bundle_root)\d0c0\d1c1\d2c0\d3c1.txt" />
        </Directory>
    </Directory>
    <Directory Name="d1c2">
        <File Source="!(bindpath.bundle_root)\d0c0\d1c2\d2c0.txt" />
    </Directory>
</Directory>
<!-- END generated XML -->
```
