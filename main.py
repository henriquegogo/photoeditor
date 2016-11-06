#!/usr/bin/env python

import os, glob, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

imagePath = "./original.jpg"
samplePath = "/usr/tmp/sample.jpg"
previewPath = "/usr/tmp/preview.jpg"

class SignalsHandler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onChangedFilter(self, combo):
        index = combo.get_active()
        model = combo.get_model()
        item = model[index][0]
        filename = model[index][1]
        commandline = 'gm convert -hald-clut {} {} -resize 640 -quality 97 {}'.format(filename, samplePath, previewPath)
        os.system(commandline)
        showImage(previewPath)

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
    if (filepath != previewPath):
        commandline = 'gm convert {} -resize 640 -quality 97 {}'.format(filepath, samplePath)
        os.system(commandline)
        filepath = samplePath
    imagePixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filepath, 640, 480)
    previewImage.set_from_pixbuf(imagePixbuf)

filtersPath = glob.glob('./filters/*/*')
for filePath in filtersPath:
    groupName = filePath.split('/')[-2].replace('_', ' ')
    fileName = filePath.split('/')[-1].split('.')[0].replace('_', ' ')
    description = '{} - {}'.format(groupName, fileName).upper()
    filePath = filePath.replace('(', '\(').replace(')', '\)')
    optionsList.append([description, filePath])

showImage(imagePath)

window.show_all()
Gtk.main()
