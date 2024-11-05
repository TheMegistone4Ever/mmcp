import logging
import os
from pathlib import Path


def find_project_root(current_path: Path, root_identifier=".git"):
    for parent in current_path.parents:
        if (parent / root_identifier).exists():
            return parent
    return current_path


PROJECT_ROOT = find_project_root(Path(__file__))
LOGS_DIR = PROJECT_ROOT / "logs"

os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / "mmcp.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

LOGGER = logging.getLogger(__name__)
LOGGER.debug(f"Logger initialized at {LOGS_DIR}...")