import os
from pathlib import Path

HOSTNAME: str = os.uname().nodename
"""Machine hostname as in `uname -n`"""

HOME: Path = Path.home()
