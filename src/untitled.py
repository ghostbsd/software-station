#!/usr/bin/python
"""ZetCode PyGTK tutorial."""

import gtk
import os

COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2


class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()

        self.set_size_request(650, 400)
        self.set_position(gtk.WIN_POS_CENTER)

        self.connect("destroy", gtk.main_quit)
        self.set_title("IconView")

        self.current_directory = '/'

        vbox = gtk.VBox(False, 0)

        toolbar = gtk.Toolbar()
        vbox.pack_start(toolbar, False, False, 0)

        self.upButton = gtk.ToolButton(gtk.STOCK_GO_UP)
        self.upButton.set_is_important(True)
        self.upButton.set_sensitive(False)
        toolbar.insert(self.upButton, -1)

        homeButton = gtk.ToolButton(gtk.STOCK_HOME)
        homeButton.set_is_important(True)
        toolbar.insert(homeButton, -1)

        self.fileIcon = self.get_icon(gtk.STOCK_FILE)
        self.dirIcon = self.get_icon(gtk.STOCK_DIRECTORY)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)

        self.store = self.create_store()
        self.fill_store()

        iconView = gtk.IconView(self.store)
        iconView.set_selection_mode(gtk.SELECTION_MULTIPLE)

        self.upButton.connect("clicked", self.on_up_clicked)
        homeButton.connect("clicked", self.on_home_clicked)

        iconView.set_text_column(COL_PATH)
        iconView.set_pixbuf_column(COL_PIXBUF)

        iconView.connect("item-activated", self.on_item_activated)
        sw.add(iconView)
        iconView.grab_focus()

        self.add(vbox)
        self.show_all()

    def get_icon(self, name):
        theme = gtk.icon_theme_get_default()
        return theme.load_icon(name, 48, 0)

    def create_store(self):
        store = gtk.ListStore(str, gtk.gdk.Pixbuf, bool)
        store.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
        return store

    def fill_store(self):
        self.store.clear()

        if self.current_directory is None:
            return

        for fl in os.listdir(self.current_directory):

            if not fl[0] == '.':
                if os.path.isdir(os.path.join(self.current_directory, fl)):
                    self.store.append([fl, self.dirIcon, True])
                else:
                    self.store.append([fl, self.fileIcon, False])

    def on_home_clicked(self, widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~'))
        self.fill_store()
        self.upButton.set_sensitive(True)

    def on_item_activated(self, widget, item):
        model = widget.get_model()
        path = model[item][COL_PATH]
        isDir = model[item][COL_IS_DIRECTORY]

        if not isDir:
            return

        self.current_directory = self.current_directory + os.path.sep + path
        self.fill_store()
        self.upButton.set_sensitive(True)

    def on_up_clicked(self, widget):
        self.current_directory = os.path.dirname(self.current_directory)
        self.fill_store()
        sensitive = True
        if self.current_directory == "/":
            sensitive = False
        self.upButton.set_sensitive(sensitive)


PyApp()
gtk.main()
