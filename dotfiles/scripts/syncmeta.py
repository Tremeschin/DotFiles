import functools
import re
import subprocess
import tomllib
from pathlib import Path

from pydantic import BaseModel


class Member(BaseModel):
    name: str
    path: Path

    @functools.cached_property
    def pyproject(self) -> dict:
        toml = self.path.joinpath("pyproject.toml").read_text()
        return tomllib.loads(toml)

    @property
    def project(self) -> dict:
        return self.pyproject["project"]

class Workspace(BaseModel):
    members: list[Member]


# Get all projects directories
workspace = Workspace.model_validate_json(subprocess.check_output((
    "uv", "workspace", "metadata",
    "--preview-features", "workspace-metadata"
)).decode())


for member in workspace.members:
    init = member.path.joinpath(member.name, "__init__.py")

    if not init.exists():
        continue

    content = init.read_text()

    for key, value in {
        "__package__": member.project.get("name"),
        "__about__":   member.project.get("description"),
        "__version__": member.project.get("version"),
        "__license__": member.project.get("license"),
    }.items():
        content = re.sub(
            rf"^(\s*{re.escape(key)}\s*=).*?$",
            rf'\1 "{value}"',
            string=content,
            flags=re.MULTILINE,
        )

    init.write_text(content)
