from pathlib import Path
from cerberus import TypeDefinition

def _check_if_exists(path: str) -> bool:
    """
    Checks if the path exists
    Args:
        path: path as string

    Returns:
        True of exists else false
    """
    return Path(path).exists()

