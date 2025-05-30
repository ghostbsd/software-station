# File: PkgDataProvider.py

from typing import List, Union
from PkgRepoSqlReader import PkgRepoSqlReader, Package
import subprocess
import sqlite3

class PkgBinaryWrapper:
    def __init__(self):
        pass

    def search_packages(self, prefix: str) -> Union[List[Package], str]:
        try:
            result = subprocess.run(
                ['pkg', 'query', '-a', '%n %v %e'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=True,
                text=True,
                timeout=10
            )
            output = result.stdout.strip().splitlines()

            installed = self.get_installed_packages()

            packages = []
            for line in output:
                parts = line.split(' ', 2)
                if len(parts) >= 2 and parts[0].startswith(prefix):
                    name, version = parts[0], parts[1]
                    desc = parts[2] if len(parts) == 3 else ''
                    packages.append(Package(
                        name=name,
                        version=version,
                        description=desc,
                        installed=(name in installed)
                    ))
            return packages
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            return f"pkg error: {e}"

    def get_installed_packages(self) -> set[str]:
        try:
            conn = sqlite3.connect("/var/db/pkg/local.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM packages")
            names = {row[0] for row in cursor.fetchall()}
            conn.close()
            return names
        except sqlite3.DatabaseError:
            return set()

class PkgDataProvider:
    def __init__(self, repo_name="GhostBSD"):
        self.repo_reader = PkgRepoSqlReader(repo_name)
        self.fallback_reader = PkgBinaryWrapper()

    def search(self, prefix: str) -> Union[List[Package], str]:
        result = self.repo_reader.search_packages(prefix)
        if isinstance(result, str):
            return self.fallback_reader.search_packages(prefix)
        return result
