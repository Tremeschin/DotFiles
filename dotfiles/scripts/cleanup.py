import shutil
from pathlib import Path

root = Path.cwd()

# Caches, artifacts
unwanted: list[str] = [
    "__pycache__",
    ".cache",
    "*.pyc",
    "site",
    "target",
]

def remove(path: Path) -> None:
    if input(f"Enter to remove ({path}) ") != "":
        return
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        path.unlink(missing_ok=True)

for matches in list(map(root.rglob, unwanted)):
    for path in matches:
        remove(path)
