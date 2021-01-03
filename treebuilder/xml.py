from collections import deque
from typing import Any, Dict
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring
from xml.dom import minidom

from treebuilder.constants import ATTRIBUTES


def to_xml_tree(tree: Dict[str, Any], root: str = None) -> ElementTree:

    if root is None:
        if len(tree) > 1:
            raise Exception(f'Xml root has to be unique, but was: {tree.keys()}')
        xml_root = None
    else:
        xml_root = Element(root)

    stack = deque()
    stack.append((tree, xml_root))
    while len(stack) > 0:
        data, xml = stack.pop()

        for entry in data:
            if entry == ATTRIBUTES:
                continue

            item = data[entry]

            if isinstance(item, list): # It's a node
                for x in item:
                    attributes = x[ATTRIBUTES] if ATTRIBUTES in x else {}

                    if xml_root is None:
                        xml_root = xml_child = Element(entry, attrib=attributes)
                    else:
                        xml_child = SubElement(xml, entry, attrib=attributes)

                    stack.append((x, xml_child))                    
            else: # It's a leaf
                xml_child = SubElement(xml, entry)
                xml_child.text = str(item)
    
    return xml_root


def to_xml_string(tree: Dict[str, Any], root: str = None, pretty: bool = True) -> str:
    xml = to_xml_tree(tree, root)
    xml_string = tostring(xml)
    if pretty:
        reparsed = minidom.parseString(xml_string)
        return reparsed.toprettyxml(indent='\t')
    return xml_string


def to_xml(tree: Dict, file_path: str, root: str = None, pretty: bool = True):
    xml_string = to_xml_string(tree, root=root, pretty=pretty)
    with open(file_path, mode='w') as f:
        f.write(xml_string)