#!/usr/bin/env python

import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

imagePath = "./original.jpg"

class SignalsHandler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onChangedFilter(self, combo):
        index = combo.get_active()
        model = combo.get_model()
        item = model[index][0]
        filename = model[index][1]
        commandline = 'gm convert -hald-clut {} {} -resize 640 -quality 97 {}'.format(filename, 'sample.jpg', 'preview.jpg')
        os.system(commandline)
        showImage('preview.jpg')

    def onButtonPressed(self, button):
        print('Saved!')

builder = Gtk.Builder()
builder.add_from_file("./application.glade")
builder.connect_signals(SignalsHandler())

window = builder.get_object("applicationWindow")
previewImage = builder.get_object("previewImage")
optionsCombo = builder.get_object("optionsCombo")
optionsList = builder.get_object("optionsList")

def showImage(filepath):
    if (filepath != 'preview.jpg'):
        commandline = 'gm convert {} -resize 640 -quality 97 sample.jpg'.format(filepath)
        os.system(commandline)
        filepath = 'sample.jpg'
    imagePixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filepath, 640, 480)
    previewImage.set_from_pixbuf(imagePixbuf)

optionsList.append(["Kodak", "kodak.png"])
optionsList.append(["Fujifilm", "fujifilm.png"])

showImage(imagePath)

window.show_all()
Gtk.main()
