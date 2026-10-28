from abc import ABC, abstractmethod
from typing import Literal

from attrs import Factory, define, field
from cyclopts import App as Cyclopts
from parsenaut.cyclopts import Launcher

type VendorCPU = Literal["amd", "intel"]
type VendorGPU = Literal["amd", "intel", "nvidia"]

@define
class Hardware:
    cpu: set[VendorCPU] = Factory(set)
    gpu: set[VendorGPU] = Factory(set)


@define
class System(ABC):
    cli: Cyclopts = field(
        factory=lambda: Launcher.chain(Cyclopts(
            result_action="return_value",
            version_flags=[],
            # help_flags=[],
            usage="",
        ),
    ))

    def __attrs_post_init__(self):
        self.commands()

    @abstractmethod
    def commands(self):
        ...
