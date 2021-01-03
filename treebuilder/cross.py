from typing import Any, Dict, List


# Todo: maybe it should be better to returns an iterable instead of a list
def cross(source: List[Dict[str, Any]], entry: str, values: List[Any]) -> List[Dict[str, Any]]:
    """Cross source with values

    Cross generate all combination between source items and values as `S x V`
    where `S` is the source length and `V` the values length.

    Examples:
        >>> import treebuilder as tb
        >>> x = [{'Name': 'foo'}, {'Name': 'bar'}]

        >>> y = tb.cross(x, 'Value', [1, 2])
        >>> print(y)

        >>> y = tb.cross(x, 'Value', [1, 2, 3])
        >>> print(y)

        >>> y = tb.cross(x, 'Value', [1])
        >>> print(y)

    Args:
        source (List[Dict[str, Any]]): Source list to cross.
        entry (str): Entry key under which values are stored.
        values (List[Any]): List of values to cross.

    Returns:
        List[Dict[str, Any]]: The crossed list with `length = S x V`.
    """
    if len(source) == 0: # Todo: Maybe not because 0 x V should be = 0 as it does for S x 0 here
        return [{ entry: v } for v in values]
    
    result = []
    if len(values) > 0:
        # First we modify the existing objects
        for item in source:
            item[entry] = values[0]
            result.append(item)

    for value in values[1:len(values)]:
        for item in source:
            copy = item.copy() # Todo: Proably need a deep copy here
            copy[entry] = value
            result.append(copy)

    return result
    
        
