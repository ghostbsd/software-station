# File: search_index.py

import bisect
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Package:
    name: str
    description: str = ""
    version: str = ""
    installed: bool = False

class PkgSearchIndex:
    def __init__(self, packages: List[Package], key: str = 'name'):
        self.key = key
        self.sorted_packages = sorted(
            packages,
            key=lambda p: getattr(p, key).casefold() if hasattr(p, key) else ""
        )
        self.sorted_keys = [
            getattr(p, key).casefold() if hasattr(p, key) else ""
            for p in self.sorted_packages
        ]

    def search_exact(self, value: str) -> Optional[Package]:
        folded_value = value.casefold()
        index = bisect.bisect_left(self.sorted_keys, folded_value)
        if index != len(self.sorted_keys) and self.sorted_keys[index] == folded_value:
            return self.sorted_packages[index]
        return None

    def search_prefix(self, prefix: str) -> List[Package]:
        folded_prefix = prefix.casefold()
        start = bisect.bisect_left(self.sorted_keys, folded_prefix)
        end = bisect.bisect_right(self.sorted_keys, folded_prefix + '\uffff')
        return self.sorted_packages[start:end]
