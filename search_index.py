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
        self.sorted_packages = sorted(packages, key=lambda p: getattr(p, key))
        self.sorted_keys = [getattr(p, key) for p in self.sorted_packages]

    def search_exact(self, value: str) -> Optional[Package]:
        index = bisect.bisect_left(self.sorted_keys, value)
        if index != len(self.sorted_keys) and self.sorted_keys[index] == value:
            return self.sorted_packages[index]
        return None

    def search_prefix(self, prefix: str) -> List[Package]:
        start = bisect.bisect_left(self.sorted_keys, prefix)
        if prefix:
            next_prefix = prefix[:-1] + chr(ord(prefix[-1]) + 1)
        else:
            next_prefix = chr(0)
        end = bisect.bisect_left(self.sorted_keys, next_prefix)
        return self.sorted_packages[start:end]
