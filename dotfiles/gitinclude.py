from os import PathLike
from pathlib import Path


def gitinclude(*paths: PathLike) -> str:
    """Generate a reverse .gitignore whitelist"""
    content: list[str] = []
    content.append("*")

    for file in sorted(map(Path, paths)):
        for path in reversed([file] + list(file.parents)[:-1]):
            content.append(f"!{path}")

    return "\n".join(content)
