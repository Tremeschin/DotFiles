from collections.abc import Iterable

from attrs import define
from dotfiles.core.system.archlinux import ArchLinux, Synckage, System


@define
class Archium(ArchLinux, System):
    """Main desktop"""

@define
class Vivobook(ArchLinux, System):
    """Main laptop"""

    def packages(self) -> Iterable[Synckage]:
        yield from ArchLinux.packages(self)
        yield Synckage("wireless-regdb")

@define
class Sweeper(ArchLinux, System):

    def packages(self) -> Iterable[Synckage]:
        yield from ArchLinux.packages(self)
        yield Synckage("intel-oneapi-mkl")
