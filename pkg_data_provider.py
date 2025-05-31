# File: pkg_data_provider.py

"""
Provides an abstraction layer to search FreeBSD/GhostBSD packages
using either a local SQLite repository or the 'pkg' binary.
"""

import subprocess
import sqlite3
from typing import List, Union

from PkgRepoSqlReader import PkgRepoSqlReader, Package


class PkgBinaryWrapper:
    """Fallback class to search packages using the 'pkg' binary tool."""


    def __init__(self):
        pass


    def search_packages(self, prefix: str) -> Union[List[Package], str]:
        """
        Searches available packages using the `pkg` command-line tool.

        Args:
            prefix (str): Package name prefix to match.

        Returns:
            Union[List[Package], str]: List of Package objects or error message.
        """
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
        """
        Retrieves installed package names from the local SQLite database.

        Returns:
            set[str]: A set of installed package names.
        """
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
    """
    Main interface to query package data from the repository or fall back
    to the pkg binary if the SQLite method fails.
    """


    def __init__(self, repo_name="GhostBSD"):
        self.repo_reader = PkgRepoSqlReader(repo_name)
        self.fallback_reader = PkgBinaryWrapper()


    def search(self, prefix: str) -> Union[List[Package], str]:
        """
        Searches for packages by prefix using repository first, then binary fallback.

        Args:
            prefix (str): Package name prefix to match.

        Returns:
            Union[List[Package], str]: A list of matched packages or an error string.
        """
        result = self.repo_reader.search_packages(prefix)
        if isinstance(result, str):
            return self.fallback_reader.search_packages(prefix)
        return result
