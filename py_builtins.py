import builtins
from dataclasses import dataclass


@dataclass
class Builtin:
    name: str


builtins_map = {builtin: Builtin(builtin) for builtin in dir(builtins)}
