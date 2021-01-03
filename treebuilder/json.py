from typing import Any, Dict
from collections import deque
import json


def to_json_tree(tree: Dict[str, Any], root: str = None) -> Dict[str, Any]:
    
    json_root = {}
    
    stack = deque()
    stack.append((tree, json_root))
    while len(stack) > 0:
        data, json_node = stack.pop()

        for entry in data:
            item = data[entry]

            if isinstance(item, list): # It's a node
                if len(item) == 1:
                    child = {}
                    json_node[entry] = child
                    stack.append((item[0], child))
                else: 
                    children = [{} for i in range(len(item))]
                    json_node[entry] = children
                    [stack.append((x, child)) for x, child in zip(item, children)]
            else: # It's a leaf
                json_node[entry] = data[entry]

    return json_root


def to_json_string(tree: Dict[str, Any], root: str = None, pretty: bool = True) -> str:
    tree = to_json_tree(tree, root)
    if pretty:
        return json.dumps(tree, indent='\t')
    return json.dumps(tree)


def to_json(tree: Dict, file_path: str, root: str = None, pretty: bool = True):
    json_string = to_json_string(tree, root=root, pretty=pretty)
    with open(file_path, mode='w') as f:
        f.write(json_string)