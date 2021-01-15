from typing import Any, Dict, List
import copy


# Todo: maybe it should be better to returns an iterable instead of a list
def expand(source: List[Dict[str, Any]], entry: str, values: List[Any], deep_copy: bool = True) -> List[Dict[str, Any]]:
    """Expand source by a values list 

    Expand generates combination of source and values one by one.

    When both source and values have the same length, the expansion is applied only
    on each source's item by setting each value to its entry key.
    If their length are differents, the expansion applies on either source and 
    values lists length.

    The shortest list rolls until reaching the end of the longer one by using a ring logic.
    A list used as a ring means that when the end of this list is reached we go back to 
    the first element then continue iteration.

    Exemples:
        >>> import treebuilder as tb
        >>> x = []
        >>> y = tb.expand(x, 'Name', ['Sapiens', 'Harry Potter', 'A Time of Mercy'])
        >>> print(y)
        >>> z = tb.expand(y, 'Id', [1, 2, 3])
        >>> print(z)

        >>> x = [{'Name': 'foo'}, {'Name': 'bar'}]
        >>> y = tb.expand(x, 'Value', [1])
        >>> print(y)
        >>> y = tb.expand(x, 'Value', [1, 2, 3])
        >>> print(y)

    Args:
        source (List[Dict[str, Any]]): Source list to expand.
        entry (str): Entry key under which values are stored.
        values (List[Any]): List of values to expand.
        deep_copy (bool): Make a deep copy on values for each usages. Default is True.

    Returns:
        List[Dict[str, Any]]: The expanded list.
    """
    if len(values) == 0:
        return source

    result = []
    # Add values as a ring to the source
    index = 0
    should_expand_source = True
    for item in source:
        if index == len(values):
            index = 0
            should_expand_source = False
        
        item[entry] = copy.deepcopy(values[index]) if deep_copy else values[index]
        index += 1
        result.append(item)

    # If values is longer than the source
    if should_expand_source:
        if len(source) > 0:
            # We ring around the source values to duplicate items then set the value
            while index < len(values):
                for item in source:
                    if index == len(values):
                        break
                    
                    clone = copy.deepcopy(item) if deep_copy else item.copy()
                    clone[entry] = copy.deepcopy(values[index]) if deep_copy else values[index]
                    index += 1
                    result.append(clone)
        else:
            # The source is empty so we build from values
            while index < len(values):
                result.append({ entry: copy.deepcopy(values[index]) if deep_copy else values[index] })
                index += 1
    
    return result
