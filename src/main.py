#!/usr/local/bin/python

import gtk as Gtk
import threading
import sys
from pkgngHandler import packagelist, softwareVersion, sotwareComment
from xpm import xpmPackageCategory, softwareXpm


class TableWindow(Gtk.Window):

    def selection_Category(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        self.pkg_store.clear()
        path = pathlist[0]
        tree_iter = model.get_iter(path)
        value = model.get_value(tree_iter, 1)
        XPM = Gtk.gdk.pixbuf_new_from_xpm_data(softwareXpm())
        for line in packagelist(value):
                liste = line.split(':')
                software = liste[0].partition('/')[2]
                # version = liste[1]
                comment = liste[1]
                self.pkg_store.append([XPM, software, comment])

    def selected_software(self, tree_selection):
        pass

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Software Station")
        self.connect("delete-event", Gtk.main_quit)
        table = Gtk.Table(16, 10, True)
        self.set_size_request(850, 500)
        self.add(table)
        button1 = Gtk.Button(label="Button 1")
        tbar = Gtk.Toolbar()
        category_sw = Gtk.ScrolledWindow()
        category_sw.set_shadow_type(Gtk.SHADOW_ETCHED_IN)
        category_sw.set_policy(Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC)
        self.store = Gtk.ListStore(Gtk.gdk.Pixbuf, str)
        self.treeview = Gtk.TreeView(self.Tree_Store())
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
        tree_selection.set_mode(Gtk.SELECTION_SINGLE)
        tree_selection.connect("changed", self.selection_Category)
        category_sw.add(self.treeview)
        category_sw.show()
        pkg_sw = Gtk.ScrolledWindow()
        pkg_sw.set_shadow_type(Gtk.SHADOW_ETCHED_IN)
        pkg_sw.set_policy(Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC)
        self.pkg_store = Gtk.ListStore(Gtk.gdk.Pixbuf,str, str)
        treeView = Gtk.TreeView(self.pkg_store)
        treeView.set_model(self.pkg_store)
        treeView.set_rules_hint(True)
        cell = Gtk.CellRendererPixbuf()
        column3 = Gtk.TreeViewColumn("Pixbuf", cell)
        column3.add_attribute(cell, "pixbuf", 0)
        treeView.append_column(column3)
        cell = Gtk.CellRendererText()
        column4 = Gtk.TreeViewColumn(None, cell, text=1)
        column4.set_sizing(Gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column4.set_fixed_width(1)
        column4.set_sort_column_id(0)
        treeView.append_column(column4)
        cell = Gtk.CellRendererText()
        column5 = Gtk.TreeViewColumn(None, cell, text=2)
        column5.set_sort_column_id(0)
        treeView.append_column(column5)
        treeView.set_headers_visible(False)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(Gtk.SELECTION_SINGLE)
        tree_selection.connect("changed", self.selected_software)
        pkg_sw.add(treeView)
        pkg_sw.show()
        state = Gtk.Statusbar()
        table.attach(tbar, 0, 10, 0, 1)
        table.attach(category_sw, 0, 2, 1, 16)
        table.attach(pkg_sw, 2, 10, 1, 11)
        table.attach(state, 2, 10, 15, 16)
        self.show_all()

    def Tree_Store(self):
        self.store.clear()
        for category in xpmPackageCategory():
            XPM = Gtk.gdk.pixbuf_new_from_xpm_data(category[1])
            self.store.append([XPM, category[0]])
        return self.store

TableWindow()
Gtk.main()