#!/usr/local/bin/python

import gtk as Gtk
import threading
import sys
from pkgngHandler import packagelist, softwareVersion, sotwareComment, pkgsearch
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
            comment = liste[1].strip()
            self.pkg_store.append([XPM, software, comment])

    def selected_software(self, tree_selection):
        pass

    def create_arrow_button(self, arrow_type, shadow_type):
        button = Gtk.Button();
        arrow = Gtk.Arrow(arrow_type, shadow_type);
        button.add(arrow)
        button.show()
        arrow.show()
        return button

    def radio_event(self, widget, toolbar):
        if self.text_button.get_active():
            toolbar.set_style(gtk.TOOLBAR_TEXT)
        elif self.icon_button.get_active():
            toolbar.set_style(gtk.TOOLBAR_ICONS)
        elif self.both_button.get_active():
            toolbar.set_style(gtk.TOOLBAR_BOTH)

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Software Station")
        self.connect("delete-event", Gtk.main_quit)
        table = Gtk.Table(16, 10, True)
        self.set_size_request(850, 500)
        self.add(table)
        button1 = Gtk.Button(label="Button 1")
        toolbar= Gtk.Toolbar()
        toolbar.set_orientation(Gtk.ORIENTATION_HORIZONTAL)
        toolbar.set_style(Gtk.TOOLBAR_BOTH)
        toolbar.set_border_width(5)

        button = self.create_arrow_button(Gtk.ARROW_LEFT, Gtk.SHADOW_IN)
        toolbar.append_widget(button,  "Go to previous Window", "Private")
        button = self.create_arrow_button(Gtk.ARROW_RIGHT, Gtk.SHADOW_OUT)
        toolbar.append_widget(button,  "Go to next Window", "Private")
        toolbar.append_space()
        iconw = Gtk.Image()
        iconw.set_from_icon_name("package_system", Gtk.ICON_SIZE_SMALL_TOOLBAR)
        both_button = toolbar.append_element(
            Gtk.TOOLBAR_CHILD_RADIOBUTTON,
            None,
            "All Software",
            "Show all software",
            "Private",
            iconw,
            self.radio_event,
            toolbar)
        toolbar.append_space()
        self.both_button = both_button
        both_button.set_active(True)
        iconw = Gtk.Image()
        iconw.set_from_icon_name("system", Gtk.ICON_SIZE_SMALL_TOOLBAR)
        text_button = toolbar.append_element(
            Gtk.TOOLBAR_CHILD_RADIOBUTTON,
            both_button,
            "Installed Software",
            "Show all installed software",
            "Private",
            iconw,
            self.radio_event,
            toolbar)
        toolbar.append_space()
        self.text_button = text_button
        self.entry = Gtk.Entry()
        self.entry.set_icon_from_icon_name(Gtk.ENTRY_ICON_PRIMARY, "search")
        self.entry.connect("key-release-event", self.on_key_release)
        toolbar.insert_widget(self.entry,  "Search Software", "Private", 12)
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
        table.attach(toolbar, 0, 10, 0, 2)
        table.attach(category_sw, 0, 2, 2, 16)
        table.attach(pkg_sw, 2, 10, 2, 11)
        table.attach(state, 2, 10, 15, 16)
        self.show_all()

    def on_key_release(self, widget, event):
        if len(widget.get_text()) > 1:
            self.pkg_store.clear()
            XPM = Gtk.gdk.pixbuf_new_from_xpm_data(softwareXpm())
            for line in pkgsearch(widget.get_text()):
                software = line.partition(' ')[0].strip()
                # version = liste[1]
                comment = line.partition(' ')[2].strip()
                print comment
                self.pkg_store.append([XPM, software, comment])

    def Tree_Store(self):
        self.store.clear()
        for category in xpmPackageCategory():
            XPM = Gtk.gdk.pixbuf_new_from_xpm_data(category[1])
            self.store.append([XPM, category[0]])
        return self.store

TableWindow()
Gtk.main()