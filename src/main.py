#!/usr/local/bin/python3
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
from gi.repository import Gtk, GdkPixbuf

# import threading
# import sys
from pkgngHandler import packagelist  # , softwareversion, sotwarecomment
from pkgngHandler import pkgsearch
from xpm import xpmPackageCategory, softwareXpm


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
        self.box1.pack_start(toolbar, True, True, 0)
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
        table = Gtk.Table(14, 10, True)
        table.show_all()
        # self.box1.pack_start(table, True, True, 0)
        mainwin = MainBook().get_model()
        self.mainstack.add_named(mainwin, "mainwin")

        self.show_all()

    def key_release(self, widget, event):
        searchs = widget.get_text()
        print(searchs)
        if len(searchs) > 1:
            MainBook().on_key_release(searchs)


class MainBook():
    """docstring for MainBook."""

    def selected_software(self, widget, path):
        model = widget.get_model()
        data = model[path][1]
        print(data)

    def tree_store(self):
        self.store.clear()
        for category in xpmPackageCategory():
            xmp = GdkPixbuf.Pixbuf.new_from_xpm_data(category[1])
            self.store.append([xmp, category[0]])
        return self.store

    def on_key_release(self, searchs):
        print(searchs)
        # if len(searchs > 1):
        self.pkg_store.clear()
        # xmp = GdkPixbuf.Pixbuf.new_from_xpm_data(softwareXpm())
        pixbuf = Gtk.IconTheme.get_default().load_icon('emblem-package', 48, 0)
        for line in pkgsearch(searchs):
            software = line.partition(' ')[0].strip()
            # version = liste[1]
            comment = line.partition(' ')[2].strip()
            self.pkg_store.append([pixbuf, software, comment])

    def selection_category(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        self.pkg_store.clear()
        path = pathlist[0]
        tree_iter = model.get_iter(path)
        value = model.get_value(tree_iter, 1)
        pixbuf = Gtk.IconTheme.get_default().load_icon('emblem-package', 48, 0)
        # xmp = GdkPixbuf.Pixbuf.new_from_xpm_data(softwareXpm())
        for line in packagelist(value):
            liste = line.split(':')
            software = liste[0].partition('/')[2]
            # version = liste[1]
            comment = liste[1].strip()
            self.pkg_store.append([pixbuf, software, comment])

    def __init__(self):
        self.table = Gtk.Table(12, 10, True)
        self.table.show_all()
        category_sw = Gtk.ScrolledWindow()
        category_sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        category_sw.set_policy(Gtk.PolicyType.AUTOMATIC,
                               Gtk.PolicyType.AUTOMATIC)
        self.store = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        self.treeview = Gtk.TreeView(self.tree_store())
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
        # self.pkgtreeview = Gtk.TreeView(self.pkg_store)
        # self.pkgtreeview.set_model(self.pkg_store)
        # self.pkgtreeview.set_rules_hint(True)
        # self.pkgtreeview.connect_after("button_press_event",
        #                                self.selected_software)
        # cell = Gtk.CellRendererPixbuf()
        # column3 = Gtk.TreeViewColumn("Pixbuf", cell)
        # column3.add_attribute(cell, "pixbuf", 0)
        # self.pkgtreeview.append_column(column3)
        # cell = Gtk.CellRendererText()
        # column4 = Gtk.TreeViewColumn(None, cell, text=1)
        # # column4.set_sizing(Gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        # column4.set_fixed_width(200)
        # column4.set_sort_column_id(0)
        # self.pkgtreeview.append_column(column4)
        # cell = Gtk.CellRendererText()
        # column5 = Gtk.TreeViewColumn(None, cell, text=2)
        # column5.set_sort_column_id(0)
        # self.pkgtreeview.append_column(column5)
        # self.pkgtreeview.set_headers_visible(False)
        # self.tree_selection = self.pkgtreeview.get_selection()
        # # self.tree_selection.set_mode(Gtk.SelectionMode.NONE)
        # # tree_selection.connect("clicked", self.selected_software)
        # pkg_sw.add(self.pkgtreeview)
        iconview = Gtk.IconView.new()
        iconview.set_model(self.pkg_store)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(1)
        iconview.connect("item-activated", self.selected_software)
        iconview.set_tooltip_column(2)
        pkg_sw.add(iconview)
        pkg_sw.show()
        state = Gtk.Statusbar()
        # table.attach(toolbar, 0, 10, 0, 2)
        self.table.attach(category_sw, 0, 2, 0, 12)
        self.table.attach(pkg_sw, 2, 10, 0, 11)
        self.table.attach(state, 2, 10, 11, 12)

    def get_model(self):
        return self.table

TableWindow()
Gtk.main()
