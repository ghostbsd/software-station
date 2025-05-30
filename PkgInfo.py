# File: PkgInfo.py

import subprocess
from search_index import Package, PkgSearchIndex

class PkgInfo:
    def __init__(self):
        self.available: list[Package] = []
        self.installed_names: set[str] = set()
        self.index = None
        self.load()

    def load(self):
        self.load_installed()
        self.load_available()

    def load_installed(self):
        try:
            result = subprocess.run(
                ['pkg', 'query', '%n'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=True,
                text=True,
                timeout=10
            )
            self.installed_names = {name.strip() for name in result.stdout.splitlines()}
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            self.installed_names = set()

    def load_available(self):
        try:
            result = subprocess.run(
                ['pkg', 'query', '-a', '%n %v %e'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=True,
                text=True,
                timeout=10
            )
            self.available = []
            for line in result.stdout.splitlines():
                parts = line.strip().split(' ', 2)
                if len(parts) >= 2:
                    name, version = parts[0], parts[1]
                    desc = parts[2] if len(parts) == 3 else ''
                    self.available.append(Package(
                        name=name,
                        version=version,
                        description=desc,
                        installed=name in self.installed_names
                    ))
            self.index = PkgSearchIndex(self.available)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            self.available = []
            self.index = None

    def search(self, prefix: str) -> list[Package]:
        return self.available if self.index is None else self.index.search_prefix(prefix)

    def get_installed(self) -> list[Package]:
        return [pkg for pkg in self.available if pkg.installed]
