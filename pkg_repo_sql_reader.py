# File: pkg_repo_sql_reader.py

"""
Provides a class to query a FreeBSD-style SQLite package repository.
Used to search available packages and detect installed ones.
"""

import sqlite3
from typing import List, Union
from dataclasses import dataclass


@dataclass
class Package:
    """
    Represents a software package entry.
    """
    name: str
    version: str
    description: str = ""
    installed: bool = False


class PkgRepoSqlReader:
    """
    Reads package metadata from the FreeBSD/GhostBSD repository SQLite database.
    """

    def __init__(self, repo_name: str, base_path: str = "/var/db/pkg/repos"):
        """
        Initializes the reader with paths to the repo and local package databases.
        """
        self.db_path = f"{base_path}/{repo_name}/db"
        self.local_db_path = "/var/db/pkg/local.sqlite"

    def is_available(self) -> bool:
        """
        Checks whether the SQLite repository database is present and valid.

        Returns:
            bool: True if the database is found and has a valid SQLite header.
        """
        try:
            with open(self.db_path, "rb") as f:
                header = f.read(16)
                return header.startswith(b"SQLite format")
        except FileNotFoundError:
            return False

    def get_installed_packages(self) -> set[str]:
        """
        Loads the names of installed packages from the local package database.

        Returns:
            set[str]: A set of installed package names.
        """
        try:
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM packages")
            installed = {row[0] for row in cursor.fetchall()}
            conn.close()
            return installed
        except (sqlite3.DatabaseError, FileNotFoundError):
            return set()

    def search_packages(self, prefix: str) -> Union[List[Package], str]:
        """
        Searches for packages in the repository that match the given prefix.

        Args:
            prefix (str): The starting string of the package name.

        Returns:
            Union[List[Package], str]: A list of matched Package objects or an error message.
        """
        if not self.is_available():
            return f"Database not found or invalid: {self.db_path}"

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, version, comment
                FROM packages
                WHERE name LIKE ?
                ORDER BY name ASC
                """,
                (prefix + '%',)
            )
            results = cursor.fetchall()
            conn.close()

            installed = self.get_installed_packages()
            return [
                Package(
                    name=row[0],
                    version=row[1],
                    description=row[2],
                    installed=(row[0] in installed)
                )
                for row in results
            ]
        except sqlite3.DatabaseError as e:
            return f"SQLite error: {e}"
