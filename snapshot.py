from pathlib import Path
from typing import List

from diff import Difference


class FileSnapshot:
    relative_path: Path
    size: int
    modification_time: int

    def __init__(self, path: Path, relative_to: Path):
        st = path.stat()
        self.relative_path = path.relative_to(relative_to)
        self.size = st.st_size
        self.modification_time = st.st_mtime

    def __eq__(self, other: object) -> bool:
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(self.relative_path) + hash(self.size) + hash(self.modification_time)


class DirectorySnapshot:
    entries: List[FileSnapshot]

    def __init__(self, path: Path):
        self.entries = [
            # Fill self.entries with actual file metadata
            # ...
        ]

    def diff(self, new_snapshot: 'DirectorySnapshot') -> Difference:
        return Difference(
            # Calculate the difference between the two snapshots
            # ...
        )
