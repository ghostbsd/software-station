#!/usr/bin/env python

"""Example of icons in a TreeView (inspired by gtk-demo Stock Item example)."""

import pygtk
pygtk.require('2.0')
import gtk
import gobject

class stock_list(gtk.TreeView):
    def __init__(self):
        gtk.TreeView.__init__(self)
        self.init_model()
        self.init_view_columns()

    def init_model(self):
        store = gtk.ListStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING)
        for attr in dir(gtk):
            if attr.startswith('STOCK_'):
                store.append((self.get_icon_pixbuf(attr), 'gtk.%s' % attr))
        self.set_model(store)

    def get_icon_pixbuf(self, stock):
        return self.render_icon(stock_id=getattr(gtk, stock),
                                size=gtk.ICON_SIZE_MENU,
                                detail=None)

    def init_view_columns(self):
        col = gtk.TreeViewColumn()
        col.set_title('Stock Items')
        render_pixbuf = gtk.CellRendererPixbuf()
        col.pack_start(render_pixbuf, expand=False)
        col.add_attribute(render_pixbuf, 'pixbuf', 0)
        render_text = gtk.CellRendererText()
        col.pack_start(render_text, expand=True)
        col.add_attribute(render_text, 'text', 1)
        self.append_column(col)

if __name__ == '__main__':
    w = gtk.Window()
    w.set_title('Stock Items')
    w.set_size_request(width=400, height=300)
    w.connect('destroy', gtk.mainquit)
    sw = gtk.ScrolledWindow()
    sw.add(stock_list())
    w.add(sw)
    w.show_all()
    gtk.mainloop()