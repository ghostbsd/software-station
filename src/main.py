#!/usr/local/bin/python3.6
"""
Copyright (c) 2017, GhostBSD. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistribution's of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistribution's in binary form must reproduce the above
   copyright notice,this list of conditions and the following
   disclaimer in the documentation and/or other materials provided
   with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES(INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib, GObject
import threading
from time import sleep

from pkgngHandler import pkgsearch, package_origin, package_dictionary
from xpm import xpmPackageCategory


class TableWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Software Station")
        self.connect("delete-event", Gtk.main_quit)
        self.set_size_request(850, 500)
        # Creating the toolbar
        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.BOTH)
        self.box1 = Gtk.VBox(False, 0)
        self.add(self.box1)
        self.box1.show()
        self.box1.pack_start(toolbar, False, False, 0)
        self.previousbutton = Gtk.ToolButton()
        self.previousbutton.set_label("Back")
        self.previousbutton.set_is_important(True)
        self.previousbutton.set_icon_name("go-previous")
        self.previousbutton.set_sensitive(False)
        toolbar.add(self.previousbutton)
        self.nextbutton = Gtk.ToolButton()
        self.nextbutton.set_label("Forward")
        self.nextbutton.set_is_important(True)
        self.nextbutton.set_icon_name("go-next")
        self.nextbutton.set_sensitive(False)
        toolbar.add(self.nextbutton)

        radiotoolbutton1 = Gtk.RadioToolButton(label="All Software")
        radiotoolbutton1.set_icon_name("package_system")
        toolbar.add(radiotoolbutton1)
        radiotoolbutton2 = Gtk.RadioToolButton(label="Isntalled Software",
                                               group=radiotoolbutton1)
        radiotoolbutton2.set_icon_name("system")
        toolbar.add(radiotoolbutton2)
        separatortoolitem = Gtk.SeparatorToolItem()
        toolbar.add(separatortoolitem)

        toolitem = Gtk.ToolItem()
        toolbar.add(toolitem)
        self.entry = Gtk.Entry()
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
                                           "search")
        self.entry.connect("key-release-event", self.key_release)
        toolitem.add(self.entry)
        # Creating a notebook to swith
        self.mainstack = Gtk.Stack()
        self.mainstack.show()
        self.mainstack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.box1.pack_start(self.mainstack, True, True, 0)

        mainwin = self.MainBook()
        self.mainstack.add_named(mainwin, "mainwin")

        # state = Gtk.Notebook()
        # state.show()
        self.pkg_statistic = Gtk.Label()

        self.pkg_statistic.set_use_markup(True)
        self.pkg_statistic.set_xalign(0.1)
        self.progress = Gtk.ProgressBar()
        self.progress.set_show_text(True)
        grid = Gtk.Grid()
        # grid.set_row_spacing(1)
        # grid.set_column_spacing(10)
        grid.set_margin_left(10)
        grid.set_margin_right(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.attach(self.pkg_statistic, 0, 0, 4, 1)
        grid.attach(self.progress, 4, 0, 6, 1)
        grid.show()
        self.box1.pack_start(grid, False, False, 0)
        self.show_all()
        self.initial_thread()

    def sync_orgin(self):
        self.pkg_origin = package_origin()

    def sync_packages(self):
        self.pkg_dictionary = package_dictionary(self.pkg_origin)

    def initial_sync(self):
        self.pkg_statistic.set_text('<small>Syncing statistic</small>')
        self.pkg_statistic.set_use_markup(True)
        self.progress.set_fraction(0.1)
        self.progress.set_text('syncing packages origins')
        self.sync_orgin()
        self.progress.set_fraction(0.3)
        self.progress.set_text('syncing packages data')
        self.sync_packages()
        self.progress.set_fraction(0.5)
        self.progress.set_text('store packages origin')
        self.category_store_sync()
        avail = self.pkg_dictionary['avail']
        msg = "Packages available:"
        self.pkg_statistic.set_text(f'<small>{msg} {avail}</small>')
        self.pkg_statistic.set_use_markup(True)
        self.progress.show()
        self.progress.set_fraction(0.7)
        self.progress.set_text('Loading all packages')
        self.store_all_pkgs()
        self.progress.set_fraction(1)
        self.progress.set_text('completed')
        sleep(1)
        self.progress.hide()

    def initial_thread(self):
        thr = threading.Thread(target=self.initial_sync, args=())
        thr.setDaemon(True)
        thr.start()

    def selected_software(self, widget, path):
        model = widget.get_model()
        data = model[path][1]
        print(data)

    def category_store_sync(self):
        self.store.clear()
        for category in self.pkg_origin:
            xmp_data = xpmPackageCategory()[category]
            xmp = GdkPixbuf.Pixbuf.new_from_xpm_data(xmp_data)
            self.store.append([xmp, category])
        # self.treeview.set_cursor(0)

    def update_progess(self, pkg_store, pixbuf, pkg, comment):
        pkg_store.append([pixbuf, pkg, comment])

    def store_all_pkgs(self):
        self.pkg_store.clear()
        pixbuf = Gtk.IconTheme.get_default().load_icon('emblem-package', 48, 0)
        pkg_d = self.pkg_dictionary['all']
        pkg_list = list(pkg_d.keys())
        pkg_list.sort()
        for pkg in pkg_list:
            comment = pkg_d[pkg]
            # self.pkg_store.append([pixbuf, pkg, comment])
            GObject.idle_add(
                self.update_progess,
                self.pkg_store,
                pixbuf,
                pkg,
                comment
            )

    def key_release(self, widget, event):
        searchs = widget.get_text()
        print(searchs)
        if len(searchs) > 1:
            self.pkg_store.clear()
            # xmp = GdkPixbuf.Pixbuf.new_from_xpm_data(softwareXpm())
            pixbuf = Gtk.IconTheme.get_default().load_icon('emblem-package', 48, 0)
            for line in pkgsearch(searchs):
                pkg_v = line.partition(' ')[0].strip()
                dash_split = pkg_v.split('-')
                num_of_dash = int(len(dash_split) - 1)
                rversion = dash_split[num_of_dash]
                software = pkg_v.replace(f'-{rversion}', '')
                # version = liste[1]
                comment = self.pkg_dictionary['all'][software]
                self.pkg_store.append([pixbuf, software, comment])

    def selection_category(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        self.pkg_store.clear()
        path = pathlist[0]
        tree_iter = model.get_iter(path)
        value = model.get_value(tree_iter, 1)
        pixbuf = Gtk.IconTheme.get_default().load_icon('emblem-package', 48, 0)
        # xmp = GdkPixbuf.Pixbuf.new_from_xpm_data(softwareXpm())
        pkg_d = self.pkg_dictionary[value]
        pkg_list = list(pkg_d.keys())
        for pkg in pkg_list:
            comment = pkg_d[pkg]
            self.pkg_store.append([pixbuf, pkg, comment])

    def MainBook(self):
        self.table = Gtk.Table(12, 10, True)
        self.table.show_all()
        category_sw = Gtk.ScrolledWindow()
        category_sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        category_sw.set_policy(Gtk.PolicyType.AUTOMATIC,
                               Gtk.PolicyType.AUTOMATIC)
        self.store = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        self.treeview = Gtk.TreeView(self.store)
        self.treeview.set_model(self.store)
        self.treeview.set_rules_hint(True)
        cell = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn("Pixbuf", cell)
        column.add_attribute(cell, "pixbuf", 0)
        self.treeview.append_column(column)
        cell2 = Gtk.CellRendererText()
        column2 = Gtk.TreeViewColumn(None, cell2, text=0)
        column2.set_attributes(cell2, text=1)
        self.treeview.append_column(column2)
        self.treeview.set_reorderable(True)
        self.treeview.set_headers_visible(False)
        tree_selection = self.treeview.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        tree_selection.connect("changed", self.selection_category)
        category_sw.add(self.treeview)
        category_sw.show()

        pkg_sw = Gtk.ScrolledWindow()
        pkg_sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        pkg_sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.pkg_store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
        self.pkgtreeview = Gtk.TreeView(self.pkg_store)
        self.pkgtreeview.set_model(self.pkg_store)
        self.pkgtreeview.set_rules_hint(True)
        self.pkgtreeview.connect_after("button_press_event",
                                       self.selected_software)
        cell = Gtk.CellRendererPixbuf()
        column3 = Gtk.TreeViewColumn("Pixbuf", cell)
        column3.add_attribute(cell, "pixbuf", 0)
        self.pkgtreeview.append_column(column3)
        cell = Gtk.CellRendererText()
        column4 = Gtk.TreeViewColumn(None, cell, text=1)
        # column4.set_sizing(Gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column4.set_fixed_width(200)
        column4.set_sort_column_id(0)
        self.pkgtreeview.append_column(column4)
        cell = Gtk.CellRendererText()
        column5 = Gtk.TreeViewColumn(None, cell, text=2)
        column5.set_sort_column_id(0)
        self.pkgtreeview.append_column(column5)
        self.pkgtreeview.set_headers_visible(False)
        self.tree_selection = self.pkgtreeview.get_selection()
        # self.tree_selection.set_mode(Gtk.SelectionMode.NONE)
        # tree_selection.connect("clicked", self.selected_software)
        pkg_sw.add(self.pkgtreeview)
        # iconview = Gtk.IconView.new()
        # iconview.set_model(self.pkg_store)
        # iconview.set_pixbuf_column(0)
        # iconview.set_text_column(1)
        # iconview.connect("item-activated", self.selected_software)
        # iconview.set_tooltip_column(2)
        # pkg_sw.add(iconview)
        pkg_sw.show()
        # table.attach(toolbar, 0, 10, 0, 2)
        self.table.attach(category_sw, 0, 2, 0, 12)
        self.table.attach(pkg_sw, 2, 10, 0, 12)
        self.show()
        return self.table

TableWindow()
Gtk.main()
