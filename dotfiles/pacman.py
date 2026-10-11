import subprocess
from functools import cache
from typing import Literal

from attrs import define

type Package = str


@define
class Helper:
    kind: Literal["pacman", "paru", "yay"] = "pacman"

    def lines(self, *args: str) -> list[str]:
        output = subprocess.check_output((self.kind, *args)).decode()
        return list(filter(None, output.splitlines()))


@define
class Pacman:

    @staticmethod
    def install(*packages: Package) -> int:
        return subprocess.check_call(("pacman", "-S", *packages))

    @staticmethod
    def installed() -> list[Package]:
        """List of all currently installed packages"""
        return subprocess.check_output(("pacman", "-Qq")).decode().splitlines()

    @staticmethod
    def orphans() -> list[Package]:
        """List of packages that are neither a dependency or explicitly installed"""
        return subprocess.check_output(("pacman", "-Qdtq")).decode().splitlines()

    @cache
    @staticmethod
    def groups() -> list[Package]:
        """List of known syncable groups from all databases"""
        return subprocess.check_output(("pacman", "-Sg")).decode().splitlines()

    @cache
    @staticmethod
    def ungroup(package: Package) -> list[Package]:
        """Unwrap a group into its package or return package as-is"""
        if package in Pacman.groups():
            return subprocess.check_output(("pacman", "-Qgq", package)).decode().splitlines()
        return [package]

    @staticmethod
    def mark(
        *packages: Package,
        kind: Literal["asdeps", "explicit"],
    ) -> None:
        subprocess.check_call(("pacman", "-D", f"--{kind}", *packages))

    @staticmethod
    def remove() -> None:
        ...

    @staticmethod
    def sync(*packages: Package) -> None:

        # Install all target packages
        Pacman.install(*packages)

        # Set all installed packages as dependencies
        Pacman.mark(*Pacman.installed(), kind="asdeps")

        # Set target packages to explicitly install
        for group in map(Pacman.ungroup, packages):
            Pacman.mark(*group, kind="explicit")

        # Remove orphans, that is, all unwanted
        Pacman.remove(*Pacman.orphans())

pacman = Pacman()
