import os
from collections.abc import Iterable
from typing import override

from attrs import Factory, define

from dotfiles.core.system import Linux, System
from dotfiles.stow import FLAVORS

from .pacman import Pacman, Pacsync, Synckage


@define
class ArchLinux(Linux, System):

    pacman: Pacman = Factory(Pacman)
    """Package manager"""

    def __attrs_post_init__(self):
        System.__attrs_post_init__(self)
        self.stow.sources.append(FLAVORS.joinpath("common"))
        self.stow.sources.append(FLAVORS.joinpath(os.uname().nodename))

    @override
    def commands(self):
        self.cli.command(self.stow.sync, name="stow")
        self.cli.command(Pacman.get_yay, name="yay")

    def packages(self) -> Iterable[Synckage]:
        yield from Pacsync.base()
