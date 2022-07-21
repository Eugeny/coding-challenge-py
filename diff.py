from dataclasses import dataclass, field
from pathlib import Path
from typing import Set


@dataclass
class Difference:
    new_files: Set[Path] = field(default_factory=set)
    changed_files: Set[Path] = field(default_factory=set)
    deleted_files: Set[Path] = field(default_factory=set)
