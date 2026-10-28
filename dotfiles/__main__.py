import sys
from pathlib import Path

from parsenaut.cyclopts import Launcher


def main():
    launcher = Launcher(keyword="System")
    launcher.smart(
        package=Path(__file__).parent,
        directories=["system"]
    )
    launcher.cli(sys.argv[1:])
