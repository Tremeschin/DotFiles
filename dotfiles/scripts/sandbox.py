"""Simple and somewhat effective bwrap sandboxing"""
import os
import shutil
import sys
from collections.abc import Iterable
from pathlib import Path

scripts = Path(__file__).parent
home = Path.home()
cwd = Path.cwd()

class Bubble:

    def tmpfs(self) -> Iterable[Path]:
        """Clean directories"""
        yield Path("/tmp")
        yield home

    def symlinks(self) -> Iterable[tuple[Path, Path]]:
        """Symlinks (real -> virtual)"""
        yield (Path("/usr/bin"), Path("/bin"))
        yield (Path("/usr/bin"), Path("/sbin"))
        yield (Path("/usr/lib"), Path("/lib"))
        yield (Path("/usr/lib"), Path("/lib64"))

    def sys_ro(self) -> Iterable[Path]:
        """System readonly bindings"""
        yield Path("/usr")
        yield Path("/etc")

    def rw(self) -> Iterable[Path]:
        """User readwrite bindings"""
        yield home.joinpath(".local/share/opencode")
        yield home.joinpath(".local/state/opencode")

    def ro(self) -> Iterable[Path]:
        """User readonly bindings"""
        yield from home.joinpath(".config/opencode").rglob("*")
        yield home.joinpath(".cache/uv")
        yield home.joinpath(".local/share/uv")
        yield home.joinpath(".rustup")

    def block(self) -> Iterable[str | None]:
        """Alias binaries to a blocked warning"""
        yield shutil.which("git")

    def args(self, *entry: str) -> list[str | Path]:
        command: list[str | Path] = []

        # Internet for agents
        command += [
            "--die-with-parent",
            "--unshare-all",
            "--share-net",
        ]

        command += [
            "--dev", "/dev",
            "--proc", "/proc",
        ]

        # Clean directories
        for path in self.tmpfs():
            command += ("--tmpfs", path)

        # Read only binds
        for path in self.ro():
            command += ("--ro-bind-try", path.resolve(), path)
        for path in self.sys_ro():
            command += ("--ro-bind", path.resolve(), path)

        # Read write binds
        for path in self.rw():
            command += ("--bind-try", path.resolve(), path)

        command += (
            "--bind", cwd, cwd,
            "--chdir", cwd
        )

        # Symlinks
        for (real, virtual) in self.symlinks():
            command.extend(("--symlink", real, virtual))

        # Block binaries
        for item in filter(None, self.block()):
            blocked = scripts.joinpath("blocked.sh")
            command += ("--ro-bind", blocked, item)
            blocked.chmod(0o755)

        # Some command or default shell
        command += entry or [os.environ.get("SHELL", "/bin/bash")]

        return command

bubble = Bubble()

def main():
    args = list(map(str, bubble.args(*sys.argv[1:])))
    os.execvp("bwrap", args)

if __name__ == "__main__":
    main()
