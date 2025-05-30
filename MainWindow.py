# File: MainWindow.py

import gi
from PkgInfo import PkgInfo

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Software Station")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        self.pkg = PkgInfo()

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

        self.display_packages(self.pkg.available)

    def on_search_entry_changed(self, entry):
        text = entry.get_text().strip()
        if text:
            packages = self.pkg.search(text)
        else:
            packages = self.pkg.available
        self.display_packages(packages)

    def display_packages(self, packages):
        for child in self.package_list.get_children():
            self.package_list.remove(child)

        for pkg in packages:
            label = Gtk.Label()
            status = " (installed)" if pkg.installed else ""
            label.set_text(f"{pkg.name} {pkg.version}{status}\n{pkg.description}")
            label.set_xalign(0)
            label.set_line_wrap(True)
            self.package_list.add(label)

        self.package_list.show_all()
