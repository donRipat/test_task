import typing
from typing import Dict
from dataclasses import dataclass


@dataclass
class FrequencyCounter:
    frequencies: typing.ClassVar[Dict[str, int]] = {}

    @classmethod
    def count(cls, source: str) -> None:
        for c in source:
            if c in cls.frequencies:
                cls.frequencies[c] += 1
            else:
                cls.frequencies[c] = 1
        return

    @classmethod
    def get(cls) -> Dict[str, int]:
        return cls.frequencies
