#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class HelloWorld:

    def __init__(self):
#        create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(500,200)
        self.window.set_title("Blog")
        
        self.exit = gtk.Button("Exit")
        self.exit.set_tooltip_text("Quit program")
        self.exit.connect("clicked", self.destroy)
        
        self.clear = gtk.Button("Clear")
        self.clear.set_tooltip_text("Clear entry")
        self.clear.connect("clicked", self.clear_entry)
        
        self.user_label = gtk.Label("Username:")
        self.mail_label = gtk.Label("Email:")
        self.user_entry = gtk.Entry()
        self.mail_entry = gtk.Entry()
        
        self.login = gtk.HBox()
        self.login.pack_start(self.user_label)
        self.login.pack_start(self.user_entry)
        
        self.email = gtk.HBox()
        self.email.pack_start(self.mail_label)
        self.email.pack_start(self.mail_entry)
        
        self.button = gtk.HBox()
        self.button.pack_start(self.exit)
        self.button.pack_start(self.clear)
        
        self.vbox = gtk.VBox()
#        self.vbox.pack_start(self.login)
#        self.vbox.pack_start(self.entry)
        self.vbox.pack_start(self.login)
        self.vbox.pack_start(self.email)
        self.vbox.pack_start(self.button)
        
        self.window.add(self.vbox)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)


#   callback
    def destroy(self, widget, data=None):
        print "Exiting program"
        gtk.main_quit()

    def main(self):
#        All PyGTK applications must have a gtk.main(). Control ends here
#        and waits for an event to occur (like a key press or mouse event).
        gtk.main()

    def clear_entry(self, widget):
        print "Clearing entry"
#print __name__
if __name__ == "__main__":
    base = HelloWorld()
    base.main()
