"""Define various miscellaneous utility functions."""
from typing import Any, Dict


def get_nearest_by_numeric_key(data: Dict[int, Any], key: int) -> Any:
    """Return the dict element whose numeric key is closest to a target."""
    return data.get(key, data[min(data.keys(), key=lambda k: abs(k - key))])
