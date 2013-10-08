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
        
        self.exit_button = gtk.Button("Exit")
        self.exit_button.set_tooltip_text("Quit program")
        self.exit_button.connect("clicked", self.destroy)
        
        self.clear_button = gtk.Button("Clear")
        self.clear_button.set_tooltip_text("Clear entry")
        self.clear_button.connect("clicked", self.clear_entry)

        self.submit_button = gtk.Button("Submit")
        self.submit_button.set_tooltip_text("Submit")
        self.submit_button.connect("clicked", self.submit)
        
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
        self.button.pack_start(self.exit_button)
        self.button.pack_start(self.clear_button)
        self.button.pack_start(self.submit_button)

        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.login)
        self.vbox.pack_start(self.email)
        self.vbox.pack_start(self.button)

        self.window.add(self.vbox)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
#        All PyGTK applications must have a gtk.main(). Control ends here
#        and waits for an event to occur (like a key press or mouse event).
        gtk.main()

#   callback
    def destroy(self, widget, data=None):
        print "Exiting program"
        gtk.main_quit()


    def clear_entry(self, widget):
        self.user_entry.set_text("")
        self.mail_entry.set_text("")
        print "Entry cleared"

    def submit(self, widget):
        print self.user_entry.get_text()
        print self.mail_entry.get_text()
        print "submit"

#print __name__
if __name__ == "__main__":
    base = HelloWorld()
    base.main()
