import os
from collections.abc import Iterable
from typing import override

from attrs import Factory, define

from dotfiles.core.archlinux.pacman import Pacman, Pacsync, Synckage
from dotfiles.stow import FLAVORS, Stow
from dotfiles.system import System


@define
class ArchLinux(System):
    pacman: Pacman = Factory(Pacman)

    stow: Stow = Factory(Stow)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.stow.sources.append(FLAVORS.joinpath("common"))
        self.stow.sources.append(FLAVORS.joinpath(os.uname().nodename))

    @override
    def commands(self):
        self.cli.command(self.sync)
        self.cli.command(self.stow.sync, name="stow")
        self.cli.command(Pacman.get_yay)

    def sync(self):
        print("packages")

    def packages(self) -> Iterable[Synckage]:
        yield from Pacsync.base()

# ---------------------------------------------------------------------------- #

@define
class Archium(ArchLinux, System):
    """Main desktop"""

@define
class Vivobook(ArchLinux, System):
    """Main laptop"""

@define
class Sweeper(ArchLinux, System):

    def packages(self) -> Iterable[Synckage]:
        yield from ArchLinux.packages(self)
        yield Synckage("intel-oneapi-mkl")
