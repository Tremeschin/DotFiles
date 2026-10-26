import os
from pathlib import Path
from typing import Literal

from attrs import Factory, define

type Hostname = Literal[
    "archium",
    "netbook",
    "sweeper",
    "vivobook",
]

type VendorCPU = Literal["amd", "intel"]
type VendorGPU = Literal["amd", "intel", "nvidia"]

@define
class Hardware:
    cpu: set[VendorCPU] = Factory(set)
    gpu: set[VendorGPU] = Factory(set)


@define
class Host:

    name: Hostname = os.uname().nodename # type: ignore
    """Machine hostname as in `uname -n`"""

    hardware: Hardware = Factory(Hardware)

    def __attrs_post_init__(self):

        # Avoid frying the CPU
        if cpuinfo := Path("/proc/cpuinfo").read_text():
            if "GenuineIntel" in cpuinfo:
                self.hardware.cpu.add("intel")
            if "AuthenticAMD" in cpuinfo:
                self.hardware.cpu.add("amd")

        # Search PCI hardware
        for device in Path("/sys/bus/pci/devices").iterdir():
            d_class  = int(device.joinpath("class" ).read_text(), 16)
            d_vendor = int(device.joinpath("vendor").read_text(), 16)

            # Display Controllers
            if d_class >> 16 == 0x03:
                if d_vendor == 0x10de: # novideo
                    self.hardware.gpu.add("nvidia")
                elif d_vendor == 0x1002:
                    self.hardware.gpu.add("amd")
                elif d_vendor == 0x8086:
                    self.hardware.gpu.add("intel")

    @property
    def laptop(self) -> bool:
        return self.name in ("vivobook",)

    @property
    def desktop(self) -> bool:
        return not self.laptop

host = Host()
