import subprocess
from typing import Literal

from attrs import define

type Package = str

@define
class Pacman:
    wrapper: Literal["pacman", "paru", "yay"] = "yay"

    def install(self, *packages: Package):
        subprocess.check_call((self.wrapper, "-S", *packages))

    def lock(self, *packages: Package) -> list[Package]:
        """Solve all package or groups for their dependencies"""
        ...

    def sync(self, *packages: Package):
        """

        """
        ...
