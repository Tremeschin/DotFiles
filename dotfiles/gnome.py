import subprocess
from subprocess import CompletedProcess
from typing import Self


class Gsettings:

    def set(self, base: str, key: str, value: str) -> CompletedProcess:
        return subprocess.run(("gsettings", "set", base, key, value))

    def font(self,
        interface: str = "Inter Medium 12",
        documents: str = "Inter Medium 12",
        monospace: str = "Comic Mono 12",
    ) -> Self:
        """Common system fonts configurations"""
        self.set("org.gnome.desktop.interface", "font-hinting", "full")
        self.set("org.gnome.desktop.interface", "font-antialiasing", "rgba")
        self.set("org.gnome.desktop.interface", "font-name", interface)
        self.set("org.gnome.desktop.interface", "document-font-name", documents)
        self.set("org.gnome.desktop.interface", "monospace-font-name", monospace)
        return self

    def theme(self,
        icons: str = "Papirus",
        accent: str = "purple",
    ) -> Self:
        self.set("org.gnome.desktop.interface", "icon-theme", icons)
        self.set("org.gnome.desktop.interface", "gtk-theme", "adw-gtk3-dark")
        self.set("org.gnome.desktop.interface", "color-scheme", "prefer-dark")
        self.set("org.gnome.desktop.interface", "accent-color", accent)
        return self

    def windows(self) -> Self:
        self.set("org.gnome.desktop.wm.preferences", "button-layout", "close,minimize,maximize:appmenu")
        self.set("org.gnome.desktop.wm.preferences", "resize-with-right-button", "true")
        return self

    def privacy(self) -> Self:
        """Minor privacy tweaks"""
        self.set("org.gnome.desktop.privacy", "remember-recent-files", "false")
        self.set("org.gnome.search-providers", "disable-external", "true")
        return self

    def annoyances(self) -> Self:
        self.set("org.gnome.tweaks", "show-extensions-notice", "false")
        self.set("org.gnome.desktop.interface", "show-battery-percentage", "true")
        self.set("org.gnome.desktop.interface", "enable-hot-corners", "false")
        self.set("org.gnome.desktop.peripherals.mouse", "accel-profile", "flat")

        #
        self.set("org.gnome.desktop.ddatetime", "automatic-timezone", "true")
        self.set("org.gnome.desktop.interface", "clock-format", "24h")
        self.set("org.gtk.settings.file-chooser", "clock-format", "24h")

        # See all apps in overview
        self.set("org.gnome.shell", "favorite-apps", "[]")

        return self

    def nautilus(self) -> Self:
        """Sane configurations for Nautilus"""
        self.set("org.gtk.settings.file-chooser", "sort-directories-first", "true")
        self.set("org.gnome.nautilus.preferences", "click-policy", "single")
        self.set("org.gnome.nautilus.preferences", "date-time-format", "detailed")
        return self

    def keybindings(self) -> Self:

        # Unique alt tab and previews
        self.set("org.gnome.desktop.wm.keybindings", "switch-applications", "[]")
        self.set("org.gnome.desktop.wm.keybindings", "switch-applications-backward", "[]")
        self.set("org.gnome.desktop.wm.keybindings", "switch-windows", "['<Alt>Tab']")
        self.set("org.gnome.desktop.wm.keybindings", "switch-windows-backward", "['<Shift><Alt>Tab']")

        # Super bindings
        self.set("org.gnome.desktop.wm.keybindings", "close", "['<Super>q']")
        self.set("org.gnome.desktop.wm.keybindings", "toggle-fullscreen", "['<Super>f']")
        self.set("org.gnome.desktop.wm.keybindings", "show-desktop", "['<Super>d']")

        return self

gsettings = Gsettings()

class Gnome:
    ...


gnome = Gnome()