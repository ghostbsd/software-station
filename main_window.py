"""Main application window for the Software Station GTK3 interface."""

# pylint: disable=no-member

import sys
import os

# Append current directory to the path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from PkgDataProvider import PkgDataProvider


class MainWindow(Gtk.Window):
    """Main GTK window displaying package search and results."""

    def __init__(self):
        """Initialize the main application window."""
        super().__init__(title="Software Station")
        self.set_border_width(10)
        self.set_default_size(800, 600)
        self.connect("destroy", Gtk.main_quit)

        self.pkg = PkgDataProvider()

        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search packages...")
        self.search_entry.connect("changed", self.on_search_entry_changed)

        self.package_list = Gtk.ListBox()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.package_list)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(self.search_entry, False, False, 0)
        vbox.pack_start(scrolled_window, True, True, 0)

        self.add(vbox)
        self.display_packages(self.pkg.search(""))

    def on_search_entry_changed(self, entry):
        """Handle changes in the search input field."""
        text = entry.get_text().strip()
        packages = self.pkg.search(text if text else "")
        self.display_packages(packages)

    def display_packages(self, packages):
        """Display the list of packages in the ListBox."""
        for child in self.package_list.get_children():
            self.package_list.remove(child)

        if isinstance(packages, str):
            label = Gtk.Label(label=packages)
            label.set_xalign(0)
            self.package_list.add(label)
        else:
            for pkg in packages:
                label = Gtk.Label()
                status = " (installed)" if pkg.installed else ""
                label.set_text(f"{pkg.name} {pkg.version}{status}\n{pkg.description}")
                label.set_xalign(0)
                label.set_line_wrap(True)
                self.package_list.add(label)

        self.package_list.show_all()
