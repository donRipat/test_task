import typing
from typing import Dict
from dataclasses import dataclass


@dataclass
class FrequencyCounter:
    """This class counts frequency of each character of the input string

    It takes previous input strings into account, so that large files can be fed up line by line
    """
    _frequencies: typing.ClassVar[Dict[str, int]] = {}

    @classmethod
    def count(cls, source: str) -> None:
        for c in source:
            if c in cls._frequencies:
                cls._frequencies[c] += 1
            else:
                cls._frequencies[c] = 1
        return

    @classmethod
    def get(cls) -> Dict[str, int]:
        return cls._frequencies
