import os
import warnings
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

warnings.filterwarnings(action="ignore", category=FutureWarning)



def load_env_vars(root_dir: Union[str, Path]) -> dict:
    """
    Load environment variables from .env.default and .env files.

    Args:
        root_dir: Root directory of the .env files.

    Returns:
        Dictionary with the environment variables.
    """

    if isinstance(root_dir, str):
        root_dir = Path(root_dir)

    load_dotenv(dotenv_path=root_dir / ".env.default")
    load_dotenv(dotenv_path=root_dir / ".env", override=True)

    return dict(os.environ)

def get_root_dir(default_value: str = ".") -> Path:
    """
    Get the root directory of the project.

    Args:
        default_value: Default value to use if the environment variable is not set.

    Returns:
        Path to the root directory of the project.
    """

    return Path(os.getenv("ML_PIPELINE_ROOT_DIR", default_value))

ROOT_DIR = get_root_dir()
KEYS = load_env_vars(root_dir=ROOT_DIR)
