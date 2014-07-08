#!/usr/local/bin/python

import gtk as Gtk
from pkgngHandler import packageCategory, packagelist
class TableWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("GhostBSD Installer")
        table = Gtk.Table(16, 10, True)
        self.add(table)
        button1 = Gtk.Button(label="Button 1")
        tbar = Gtk.Toolbar()
        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.SHADOW_ETCHED_IN)
        sw.set_policy(Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC)
        self.store = Gtk.TreeStore(str)
        self.Tree_Store()
        self.treeview = Gtk.TreeView(self.store)
        self.treeview.set_model(self.store)
        self.treeview.set_rules_hint(True)
        cell = Gtk.CellRendererText()
        cell.set_property('cell-background', 'white')
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label("  Available Software")
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        column.set_attributes(cell, text=0)
        self.treeview.append_column(column)
        self.treeview.set_reorderable(True)
        tree_selection = self.treeview.get_selection()
        tree_selection.set_mode(Gtk.SELECTION_SINGLE)
        #tree_selection.connect("changed", self.partition_selection)
        sw.add(self.treeview)
        sw.show()
        button3 = Gtk.Button(label="Button 3")
        state = Gtk.Statusbar()
        table.attach(tbar, 0, 10, 0, 1)
        table.attach(sw, 0, 3, 1, 16)
        table.attach(button3, 3, 10, 1, 11)
        table.attach(state, 3, 10, 15, 16)

    def Tree_Store(self):
        self.store.clear()
        for category in packageCategory():
            piter = self.store.append(None, [category])
            for line in packagelist():
                cat = line.split('/')[0]
                pkg = line.split('/')[1].rstrip()
                if cat == category:
                    self.store.append(piter, [pkg])
        return self.store

win = TableWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()