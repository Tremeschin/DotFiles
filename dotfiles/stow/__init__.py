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
    """Root directory to sync sources"""

    sources: list[Path] = Factory(list)
    """Ordered directories to sync"""

    @property
    def tracker(self) -> Path:
        """Symlinked known files tracker"""
        return self.target.joinpath(".stow")

    def files(self) -> Iterable[Path]:
        """Get managed dotfiles"""

        # Stable source path fragments in managed files
        stable: set[str] = {"DotFiles", "dotfiles"}

        for item in map(Path, self.tracker.read_text().splitlines()):
            if not item.is_symlink():
                continue

            # Check for all fragments in resolved paths
            if not set(item.resolve().parts) >= stable:
                continue

            yield item

    def dangling(self) -> Iterable[Path]:
        """Get broken links"""
        for item in self.files():
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

        # Manage manifest
        if not dry:
            for path in self.dangling():
                path.unlink()
            data = '\n'.join(sorted(map(str, seen)))
            self.tracker.write_text(data)
