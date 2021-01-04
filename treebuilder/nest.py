from typing import Any, Dict, List
from treebuilder.expand import expand


def nest(source: List[Dict[str, Any]], entry: str, values: List[Any], deep_copy: bool = True) -> List[Dict[str, Any]]:
    """Nest source by a values list.

    Nest generates combination of source and values one by one.

    When both source and values have the same length, the expansion is applied only
    on each source's item by setting each value to its entry key.

    The values list length is truncated by the source length, so the result length
    will always be equals to the source length.

    Args:
        source (List[Dict[str, Any]]): Source list to nest.
        entry (str): Entry key under which values are stored.
        values (List[Any]): List of values to nest.
        deep_copy (bool): Make a deep copy on values for each usages. Default is True.

    Returns:
        List[Dict[str, Any]]: The nested list.
    """
    if len(values) > len(source):
        values = values[0:len(source)]
    return expand(source, entry, values, deep_copy)