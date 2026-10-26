import contextlib
import shutil
import subprocess
from collections.abc import Iterable
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal

from attrs import Factory, define

type Package = str

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

    def install(self, *packages: Package):
        subprocess.check_call((self.helper, "-S", "--needed", *packages))

    @staticmethod
    def remove(*packages: Package):
        subprocess.check_call(("sudo", "pacman", "-Rns", "--confirm", *packages))

    @staticmethod
    def installed() -> list[Package]:
        """List of all currently installed packages"""
        return subprocess.check_output(("pacman", "-Qq")).decode().splitlines()

    @staticmethod
    def orphans() -> list[Package]:
        """List of packages that are neither a dependency or explicitly installed"""
        with contextlib.suppress(subprocess.CalledProcessError):
            return subprocess.check_output(("pacman", "-Qdttq")).decode().splitlines()
        return []

    @staticmethod
    def mark(*packages: Package, kind: Literal["asdeps", "asexplicit"]) -> None:
        """Set the install reason for packages"""
        subprocess.check_call(("sudo", "pacman", "-D", f"--{kind}", "--quiet", *packages))

    def sync(self, *packages: Package):
        self.install(*packages)
        self.mark(*self.installed(), kind="asdeps")
        self.mark(*packages, kind="asexplicit")

        if orphans := self.orphans():
            print(f"\nOrphans {orphans}\n")
            self.remove(*orphans)

pacman = Pacman(helper="yay")
pacman.get_yay()

# ---------------------------------------------------------------------------- #

@define
class Plan:
    target: set[str] = Factory(set)

    def __attrs_post_init__(self):
        self.target.update(set(self.apps()))
        self.target.update(set(self.audio()))
        self.target.update(set(self.aur()))
        self.target.update(set(self.base()))
        self.target.update(set(self.development()))
        self.target.update(set(self.drivers()))
        self.target.update(set(self.fonts()))
        self.target.update(set(self.games()))
        self.target.update(set(self.gnome()))
        self.target.update(set(self.terminal()))

    def base(self) -> Iterable[Package]:
        yield "7zip"
        yield "base-devel"
        yield "base"
        yield "linux-firmware"
        yield "linux"
        yield "man-db"
        yield "net-tools"
        yield "networkmanager"
        yield "realtime-privileges"
        yield "sshfs"
        yield "time"
        yield "tree"
        yield "ufw"
        yield "wget"
        yield "zip"
        yield "zram-generator"

    def aur(self) -> Iterable[Package]:
        yield "downgrade"
        yield "gnome-shell-extension-dash-to-dock"
        yield "pcsx2-git"
        yield "qview"
        yield "yay-bin"

    def audio(self) -> Iterable[Package]:
        yield "calf"
        yield "easyeffects"
        yield "gst-libav"
        yield "gst-plugin-pipewire"
        yield "gst-plugins-base"
        yield "gst-plugins-good"
        yield "gst-plugins-ugly"
        yield "pavucontrol"
        yield "pipewire-alsa"
        yield "pipewire-jack"
        yield "pipewire-pulse"
        yield "pipewire"
        yield "rhythmbox"
        yield "wireplumber"

    def apps(self) -> Iterable[Package]:
        yield "discord"
        yield "firefox"
        yield "inkscape"
        yield "librewolf"
        yield "mpv"
        yield "mullvad-vpn"
        yield "obs-studio"
        yield "profile-sync-daemon"
        yield "qbittorrent"
        yield "syncthing"
        yield "telegram-desktop"
        yield "torbrowser-launcher"

    def gnome(self) -> Iterable[Package]:
        yield "adw-gtk-theme"
        yield "baobab"
        yield "extension-manager"
        yield "ffmpegthumbnailer"
        yield "file-roller"
        yield "gdm"
        yield "gnome-console"
        yield "gnome-control-center"
        yield "gnome-desktop"
        yield "gnome-disk-utility"
        yield "gnome-keyring"
        yield "gnome-session"
        yield "gnome-shell-extension-appindicator"
        yield "gnome-shell-extensions"
        yield "gnome-shell"
        yield "gnome-tweaks"
        yield "mission-center"
        yield "mutter"
        yield "nautilus"
        yield "papers"
        yield "papirus-icon-theme"
        yield "power-profiles-daemon"

    def terminal(self) -> Iterable[Package]:
        yield "aria2"
        yield "cargo-deny"
        yield "cargo-msrv"
        yield "cargo-nextest"
        yield "cargo-outdated"
        yield "code"
        yield "croc"
        yield "evtest"
        yield "fastfetch"
        yield "fish"
        yield "git"
        yield "htop"
        yield "hyperfine"
        yield "imagemagick"
        yield "maturin"
        yield "mediainfo"
        yield "meson"
        yield "micro"
        yield "miniserve"
        yield "nano"
        yield "ollama-vulkan"
        yield "ollama"
        yield "ollama"
        yield "onefetch"
        yield "opencode"
        yield "ruff"
        yield "rust-analyzer"
        yield "rustup"
        yield "starship"
        yield "tealdeer"
        yield "tectonic"
        yield "tinymist"
        yield "tokei"
        yield "ty"
        yield "typst"
        yield "uv"
        yield "yt-dlp"
        yield "zed"
        yield "zoxide"

    def development(self) -> Iterable[Package]:
        yield "mingw-w64-binutils"
        yield "mingw-w64-crt"
        yield "mingw-w64-gcc"
        yield "mingw-w64-headers"
        yield "mingw-w64-winpthreads"
        yield "openblas"

    def fonts(self) -> Iterable[Package]:
        yield "inter-font"
        yield "noto-fonts-cjk"
        yield "noto-fonts-emoji"
        yield "otf-font-awesome"
        yield "ttf-cascadia-code-nerd"
        yield "ttf-nunito"

    def games(self) -> Iterable[Package]:
        yield "steam"
        yield "warzone2100"

    def drivers(self) -> Iterable[Package]:
        yield "mesa-utils"
        yield "mesa"
        yield "vulkan-headers"

        match host.hardware.cpu:
            case "amd":
                yield "amd-ucode"
            case "intel":
                yield "intel-ucode"
            case _:
                pass

        if host.hardware.gpu == "nvidia":
            yield "cuda"
            yield "cudnn"
            yield "lib32-nvidia-utils"
            yield "nvidia-open"
            yield "nvidia-utils"

        # Avoid frying the CPU
        if cpuinfo := Path("/proc/cpuinfo").read_text():
            if "GenuineIntel" in cpuinfo:
                yield "intel-ucode"
            if "AuthenticAMD" in cpuinfo:
                yield "amd-ucode"


def main():
    dutch = Plan()
    pacman.sync(*sorted(dutch.target))

if __name__ == "__main__":
    main()
