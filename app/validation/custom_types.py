from pathlib import Path
from cerberus import TypeDefinition

def _check_if_path_exists(path: str) -> bool:
    """
    Checks if the path exists
    Args:
        path: path as string

    Returns:
        True of exists else false
    """
    if not Path(path).exists():
        raise FileNotFoundError('Did not find a file.')
    return True

ExistingPath = TypeDefinition('existing_path', (_check_if_path_exists,), ())