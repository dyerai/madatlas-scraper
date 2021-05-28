from dataclasses import dataclass


@dataclass
class Subject:
    name: str
    abbrev: str
    code: int
