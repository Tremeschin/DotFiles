from collections.abc import Iterable
from pathlib import Path

from attrs import Factory, define

FLAVORS: Path = Path(__file__).parent
"""Common directory storing dotfiles"""

@define
class Stow:
    """
    Symlink and sync all source dotfiles into target trees:
    - Prioritizes the first relative file in sources
    - Automatic conversion if contents are the same
    - Intentionally doesn't support adoption
    """

    target: Path = Factory(Path.home)

    sources: list[Path] = Factory(list)

    @staticmethod
    def get_dotfiles(path: Path) -> Iterable[Path]:
        """Find all managed dotfiles in a path"""
        for item in path.rglob("*"):
            if not item.is_symlink():
                continue

            # Stable source path fragments in managed files
            stable: set[str] = {"DotFiles", "dotfiles"}

            # Check for all fragments in resolved paths
            if not set(item.resolve().parts) >= stable:
                continue

            yield item

    @staticmethod
    def get_dangling(path: Path) -> Iterable[Path]:
        """Find all managed dotfiles with broken links"""
        for item in Stow.get_dotfiles(path):
            try:
                item.resolve(strict=True)
            except FileNotFoundError:
                yield item

    def sync(self, dry: bool=False):

        # Safety checks
        if any(self.target.is_relative_to(x) for x in self.sources):
            raise RuntimeError("Cannot sync to a path inside sources")

        def status(kind: str) -> None:
            nonlocal dotfile, item
            print(f"{kind} ({dotfile}) -> ({item})")

        # Visited relative dotfiles
        seen: set[Path] = set()

        for root in self.sources:
            if not root.exists():
                continue
            for item in root.rglob("*"):
                if item.is_dir():
                    continue

                relative = item.relative_to(root)
                dotfile = self.target.joinpath(relative)

                # Skips and priority
                if relative in seen:
                    status("Skip")
                    continue

                seen.add(relative)

                # Skip symlinks already pointing to the right place
                if dotfile.is_symlink():
                    if (dotfile.resolve() == item):
                        status("Pass")
                        continue

                # Check for conversion or adoption
                elif dotfile.exists():

                    # Contents can already be the same, convert to symlink
                    if dotfile.read_bytes() == item.read_bytes():
                        status("Conv")
                        if not dry:
                            dotfile.unlink()
                    else:
                        raise RuntimeError(f"Detached file • adopt it {dotfile}")

                status("Link")

                # Actually create the symlink
                if not dry:
                    dotfile.parent.mkdir(parents=True, exist_ok=True)
                    dotfile.symlink_to(item)
