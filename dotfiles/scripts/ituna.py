import os
import subprocess
import sys
from subprocess import PIPE
from tempfile import NamedTemporaryFile


def main():
    with NamedTemporaryFile(prefix="tuna-") as file:
        with open(file.name, "w") as stderr:

            # Main command
            env = os.environ.copy()
            env["PYTHONPROFILEIMPORTTIME"] = "1"
            subprocess.run(
                args=sys.argv[1:],
                stderr=stderr,
                stdout=PIPE,
                check=False,
                env=env,
            )

            # Visualize
            subprocess.run(
                args=("tuna", file.name),
                check=True,
            )
