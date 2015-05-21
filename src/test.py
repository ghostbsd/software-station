#!/usr/bin/env python

import gtk
from xpm import xpmPackageCategory
window = gtk.Window()

liststore = gtk.ListStore(gtk.gdk.Pixbuf)
for f in xpmPackageCategory():
    i = gtk.gdk.pixbuf_new_from_xpm_data(f[1])
    liststore.append([i])

treeview = gtk.TreeView(liststore)
cell = gtk.CellRendererPixbuf()
column = gtk.TreeViewColumn("Pixbuf", cell)
column.add_attribute(cell, "pixbuf", 0)
treeview.append_column(column)

window.connect("destroy", lambda w: gtk.main_quit())

window.add(treeview)
window.show_all()

gtk.main()