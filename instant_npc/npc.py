from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Attribute:
    kept: List[int]
    dropped: List[int]
    modifiers: Dict[str, int]

    def get_total(self):
        total = sum(self.kept) + sum(self.modifiers.values())


@dataclass
class NPC():
    attributes: Dict[str, Attribute]
    height: HeightData