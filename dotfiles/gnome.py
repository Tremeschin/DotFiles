import subprocess
from subprocess import CompletedProcess
from typing import Self


class Gsettings:

    def set(self, base: str, key: str, value: str) -> int:
        return subprocess.check_call(("gsettings", "set", base, key, value))

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
        accent: str = "blue",
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
        self.set("org.gnome.desktop.search-providers", "disable-external", "true")
        return self

    def annoyances(self) -> Self:
        self.set("org.gnome.tweaks", "show-extensions-notice", "false")
        self.set("org.gnome.desktop.interface", "show-battery-percentage", "true")
        self.set("org.gnome.desktop.interface", "enable-hot-corners", "false")
        self.set("org.gnome.desktop.peripherals.mouse", "accel-profile", "flat")

        self.set("org.gnome.desktop.datetime", "automatic-timezone", "true")
        self.set("org.gnome.desktop.interface", "clock-format", "24h")
        self.set("org.gtk.gtk4.settings.file-chooser", "clock-format", "24h")

        # See all apps in overview
        self.set("org.gnome.shell", "favorite-apps", "[]")

        return self

    def nautilus(self) -> Self:
        """Sane configurations for Nautilus"""
        self.set("org.gtk.gtk4.settings.file-chooser", "sort-directories-first", "true")
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

    def extensions(self) -> Self:
        self.set("org.gnome.shell", "enabled-extensions", str([
            "appindicatorsupport@rgcjonas.gmail.com",
            "dash-to-dock@micxgx.gmail.com",
            "launch-new-instance@gnome-shell-extensions.gcampax.github.com",
        ]))
        return self

    def ext_dash_to_dock(self) -> Self:
        base = "org.gnome.shell.extensions.dash-to-dock"
        self.set(base, "apply-custom-theme", "false")
        self.set(base, "custom-theme-shrink", "true")
        self.set(base, "customize-alphas", "true")
        self.set(base, "dance-urgent-applications", "false")
        self.set(base, "disable-overview-on-startup", "true")
        self.set(base, "hotkeys-overlay", "false")
        self.set(base, "hotkeys-show-dock", "false")
        self.set(base, "max-alpha", "0.80")
        self.set(base, "min-alpha", "0.15")
        self.set(base, "multi-monitor", "true")
        self.set(base, "shortcut-text", "")
        self.set(base, "show-mounts", "false")
        self.set(base, "show-show-apps-button", "true")
        self.set(base, "show-trash", "false")
        self.set(base, "transparency-mode", "DYNAMIC")
        return self

    def pinned_apps(self) -> Self:
        self.set("org.gnome.shell", "favorite-apps", str([
            "firefox.desktop",
            "org.gnome.Nautilus.desktop",
            "org.pulseaudio.pavucontrol.desktop",
            "com.github.wwmm.easyeffects.desktop",
            "io.missioncenter.MissionCenter.desktop",
            "org.gnome.Console.desktop",
            "dev.zed.Zed.desktop",
            "discord.desktop",
            "org.telegram.desktop.desktop",
            "steam.desktop",
        ]))
        return self

gsettings = Gsettings()

class Gnome:
    ...

gnome = Gnome()
