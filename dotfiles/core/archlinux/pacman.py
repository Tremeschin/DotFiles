import contextlib
import shutil
import subprocess
from collections.abc import Iterable
from tempfile import TemporaryDirectory
from typing import Literal

from attrs import Factory, define

type PackageName = str

@define
class Pacman:
    helper: Literal["pacman", "paru", "yay"] = "pacman"

    @staticmethod
    def get_yay():
        if shutil.which("yay"):
            return

        if shutil.which("git") is None:
            subprocess.check_call(("sudo", "pacman", "-Sy", "git"))

        with TemporaryDirectory(prefix="yay-git-") as path:
            subprocess.check_call(("git", "clone", "https://aur.archlinux.org/yay-bin.git", path))
            subprocess.check_call(("makepkg", "-si"), cwd=path)

    def install(self, *packages: PackageName):
        subprocess.check_call((self.helper, "-S", "--needed", *packages))

    @staticmethod
    def remove(*packages: PackageName):
        subprocess.check_call(("sudo", "pacman", "-Rns", "--confirm", *packages))

    @staticmethod
    def installed() -> list[PackageName]:
        """List of all currently installed packages"""
        return subprocess.check_output(("pacman", "-Qq")).decode().splitlines()

    @staticmethod
    def orphans() -> list[PackageName]:
        """List of packages that are neither a dependency or explicitly installed"""
        with contextlib.suppress(subprocess.CalledProcessError):
            return subprocess.check_output(("pacman", "-Qdttq")).decode().splitlines()
        return []

    @staticmethod
    def mark(*packages: PackageName, kind: Literal["asdeps", "asexplicit"]) -> None:
        """Set the install reason for packages"""
        subprocess.check_call((
            "sudo", "pacman", "-D", f"--{kind}", "--quiet",
            *(x for x in packages if x in Pacman.installed())
        ))

# ---------------------------------------------------------------------------- #

@define(hash=False)
class Synckage:
    """Pacsync metadata"""

    name: PackageName

    def __hash__(self) -> int:
        return hash(self.name)

    aur: bool = False
    """Sources from AUR"""

    optional: bool = False
    """Neither sync or remove (dangle)"""


@define
class Pacsync:
    target: set[Synckage] = Factory(set)

    def __attrs_post_init__(self):
        self.target.update(self.apps())
        self.target.update(self.audio())
        self.target.update(self.aur())
        self.target.update(self.base())
        self.target.update(self.development())
        self.target.update(self.drivers())
        self.target.update(self.fonts())
        self.target.update(self.games())
        self.target.update(self.gnome())
        self.target.update(self.terminal())

    def sync(self, pacman: Pacman):
        pacman.install(*(pkg.name for pkg in self.target if not pkg.optional))
        pacman.mark(*pacman.installed(), kind="asdeps")
        pacman.mark(*(pkg.name for pkg in self.target), kind="asexplicit")

        if orphans := pacman.orphans():
            print(f"\nOrphans {orphans}\n")
            pacman.remove(*orphans)

    @staticmethod
    def base() -> Iterable[Synckage]:
        yield Synckage("7zip")
        yield Synckage("base-devel")
        yield Synckage("base")
        yield Synckage("linux-firmware")
        yield Synckage("linux")
        yield Synckage("man-db")
        yield Synckage("net-tools")
        yield Synckage("networkmanager")
        yield Synckage("ntfs-3g")
        yield Synckage("realtime-privileges")
        yield Synckage("rtkit")
        yield Synckage("sshfs")
        yield Synckage("time")
        yield Synckage("tree")
        yield Synckage("ufw")
        yield Synckage("wget")
        yield Synckage("zip")
        yield Synckage("zram-generator")

        if host.laptop:
            yield Synckage("wireless-regdb")

    @staticmethod
    def aur() -> Iterable[Synckage]:
        yield Synckage("downgrade", aur=True)
        yield Synckage("gnome-shell-extension-dash-to-dock", aur=True)
        yield Synckage("pcsx2-git", aur=True)
        yield Synckage("qview", aur=True)
        yield Synckage("yay-bin", aur=True)

    @staticmethod
    def audio() -> Iterable[Synckage]:
        yield Synckage("calf")
        yield Synckage("easyeffects")
        yield Synckage("gst-libav")
        yield Synckage("gst-plugin-pipewire")
        yield Synckage("gst-plugins-base")
        yield Synckage("gst-plugins-good")
        yield Synckage("gst-plugins-ugly")
        yield Synckage("pavucontrol")
        yield Synckage("pipewire-alsa")
        yield Synckage("pipewire-jack")
        yield Synckage("pipewire-pulse")
        yield Synckage("pipewire")
        yield Synckage("rhythmbox")
        yield Synckage("wireplumber")

    @staticmethod
    def apps() -> Iterable[Synckage]:
        yield Synckage("code")
        yield Synckage("discord")
        yield Synckage("firefox")
        yield Synckage("inkscape")
        yield Synckage("keepassxc")
        yield Synckage("libreoffice-fresh")
        yield Synckage("librewolf")
        yield Synckage("mpv")
        yield Synckage("mullvad-vpn")
        yield Synckage("obs-studio")
        yield Synckage("obsidian")
        yield Synckage("profile-sync-daemon")
        yield Synckage("qbittorrent")
        yield Synckage("syncthing")
        yield Synckage("telegram-desktop")
        yield Synckage("torbrowser-launcher")
        yield Synckage("zed")

    @staticmethod
    def gnome() -> Iterable[Synckage]:
        yield Synckage("adw-gtk-theme")
        yield Synckage("baobab")
        yield Synckage("bluez-utils")
        yield Synckage("decibels")
        yield Synckage("extension-manager")
        yield Synckage("ffmpegthumbnailer")
        yield Synckage("file-roller")
        yield Synckage("gdm")
        yield Synckage("gnome-console")
        yield Synckage("gnome-control-center")
        yield Synckage("gnome-desktop")
        yield Synckage("gnome-disk-utility")
        yield Synckage("gnome-keyring")
        yield Synckage("gnome-session")
        yield Synckage("gnome-shell-extension-appindicator")
        yield Synckage("gnome-shell-extensions")
        yield Synckage("gnome-shell")
        yield Synckage("gnome-tweaks")
        yield Synckage("mission-center")
        yield Synckage("mutter")
        yield Synckage("nautilus")
        yield Synckage("papers")
        yield Synckage("papirus-icon-theme")
        yield Synckage("power-profiles-daemon")

    @staticmethod
    def terminal() -> Iterable[Synckage]:
        yield Synckage("aria2")
        yield Synckage("croc")
        yield Synckage("evtest")
        yield Synckage("fastfetch")
        yield Synckage("fish")
        yield Synckage("git")
        yield Synckage("htop")
        yield Synckage("hyperfine")
        yield Synckage("imagemagick")
        yield Synckage("mediainfo")
        yield Synckage("micro")
        yield Synckage("miniserve")
        yield Synckage("nano")
        yield Synckage("ollama-vulkan")
        yield Synckage("ollama")
        yield Synckage("onefetch")
        yield Synckage("opencode")
        yield Synckage("ruff")
        yield Synckage("rust-analyzer")
        yield Synckage("scrcpy")
        yield Synckage("starship")
        yield Synckage("tealdeer")
        yield Synckage("tectonic")
        yield Synckage("tinymist")
        yield Synckage("tokei")
        yield Synckage("ty")
        yield Synckage("typst")
        yield Synckage("typstyle")
        yield Synckage("uv")
        yield Synckage("yt-dlp")
        yield Synckage("zoxide")

    @staticmethod
    def development() -> Iterable[Synckage]:
        yield Synckage("cargo-deny")
        yield Synckage("cargo-msrv")
        yield Synckage("cargo-nextest")
        yield Synckage("cargo-outdated")
        yield Synckage("maturin")
        yield Synckage("meson")
        yield Synckage("mingw-w64-binutils")
        yield Synckage("mingw-w64-crt")
        yield Synckage("mingw-w64-gcc")
        yield Synckage("mingw-w64-headers")
        yield Synckage("mingw-w64-winpthreads")
        yield Synckage("mold")
        yield Synckage("openblas")
        yield Synckage("wild")
        yield Synckage("rustup")

    @staticmethod
    def fonts() -> Iterable[Synckage]:
        yield Synckage("inter-font")
        yield Synckage("noto-fonts-cjk")
        yield Synckage("noto-fonts-emoji")
        yield Synckage("otf-font-awesome")
        yield Synckage("ttf-cascadia-code-nerd")
        yield Synckage("ttf-nunito")

    @staticmethod
    def games() -> Iterable[Synckage]:
        yield Synckage("prismlauncher", optional=True)
        yield Synckage("steam")
        yield Synckage("warzone2100", optional=True)

    def nvidia() -> Iterable[Synckage]:
        yield Synckage("cuda")
        yield Synckage("nvidia-open")
        yield Synckage("nvidia-utils")
        yield Synckage("lib32-nvidia-utils")

    @staticmethod
    def drivers() -> Iterable[Synckage]:
        yield Synckage("vulkan-headers")

        for vendor in host.hardware.cpu:
            if vendor == "amd":
                yield Synckage("amd-ucode")
            elif vendor == "intel":
                yield Synckage("intel-ucode")

        for vendor in host.hardware.gpu:
            if vendor == "nvidia":
                yield from Pacsync.nvidia()
            elif vendor == "amd":
                yield Synckage("mesa")
                yield Synckage("vulkan-radeon")
            elif vendor == "intel":
                yield Synckage("mesa")
                yield Synckage("vulkan-intel")
