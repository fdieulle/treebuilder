import itertools
from typing import Any, Dict, List


def expand(source: List[Dict[str, Any]], entry: str, values: List[Any]) -> List[Dict[str, Any]]:
    if len(values) == 0:
        return source

    result = []
    # Add values as a ring to the sources
    # Todo: Perf here could we use zip builtin function instead ?
    index = 0
    has_any_item = False
    should_add_new_items = True
    for item in source:
        has_any_item = True
        if index == len(values):
            index = 0
            should_add_new_items = False
        
        item[entry] = values[index]
        index += 1
        result.append(item)

    # If the values is longer than the source
    if should_add_new_items:
        if has_any_item:
            # We ring around the source valuse to duplicate then set the value
            while index < len(values):
                for item in source:
                    if index == len(values):
                        break
                    copy = item.copy() # Todo: Proably need a deep copy here
                    copy[entry] = values[index]
                    index += 1
                    result.append(copy)
        else:
            # The source is empty so we build full new values
            while index < len(values):
                result.append({ entry: values[index] })
                index += 1
    
    return result
