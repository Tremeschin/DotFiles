import os
from pathlib import Path
from typing import Literal

from attrs import Factory, define


@define
class Hardware:
    cpu: Literal["amd", "intel"] | None = None
    gpu: Literal["intel", "amd", "nvidia"] | None = None


@define
class Host:

    name: Literal[
        "archium",
        "netbook",
        "sweeper",
        "vivobook",
    ] = os.uname().nodename # type: ignore
    """Machine hostname as in `uname -n`"""

    hardware: Hardware = Factory(Hardware)

    def __attrs_post_init__(self):

        # Avoid frying the CPU
        if cpuinfo := Path("/proc/cpuinfo").read_text():
            if "GenuineIntel" in cpuinfo:
                self.hardware.cpu = "intel"
            if "AuthenticAMD" in cpuinfo:
                self.hardware.cpu = "amd"

        # Search PCI hardware
        for device in Path("/sys/bus/pci/devices").iterdir():
            d_class  = int(device.joinpath("class" ).read_text(), 16)
            d_vendor = int(device.joinpath("vendor").read_text(), 16)

            # Display Controllers
            if d_class >> 16 == 0x03:
                if d_vendor == 0x10de: # novideo
                    self.hardware.gpu = "nvidia"

host = Host()
