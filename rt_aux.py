#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  rt_aux.py
#  
#  Copyright 2018 Unknown <root@hp425>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GLib, GooCanvas, GdkPixbuf
from PIL import Image
from os import getcwd
import pdb

CONFIG_FILE = "config.xml"

#~  ____  _      ____         __           ___                            
#~ |  _ \(_)_  _| __ ) _   _ / _|         |_ _|_ __ ___   __ _  __ _  ___ 
#~ | |_) | \ \/ /  _ \| | | | |_   _____   | || '_ ` _ \ / _` |/ _` |/ _ \
#~ |  __/| |>  <| |_) | |_| |  _| |_____|  | || | | | | | (_| | (_| |  __/
#~ |_|   |_/_/\_\____/ \__,_|_|           |___|_| |_| |_|\__,_|\__, |\___|
#~                                                             |___/      

def pixbuf2image(pix):
    """Convert gdkpixbuf to PIL image"""
    data = pix.get_pixels()
    w = pix.props.width
    h = pix.props.height
    stride = pix.props.rowstride
    mode = "RGB"
    if pix.props.has_alpha == True:
        mode = "RGBA"
    im = Image.frombytes(mode, (w, h), data, "raw", mode, stride)
    return im


def image2pixbuf(im):
    """Convert Pillow image to GdkPixbuf"""
    data = im.tobytes()
    w, h = im.size
    data = GLib.Bytes.new(data)
    pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
            False, 8, w, h, w * 3)
    return pix


def do_gamma(im, gamma):
    """Fast gamma correction with PIL's image.point() method"""
    inverted_gamma = 1.0/gamma
    lut = [pow(x/255., inverted_gamma) * 255 for x in range(256)]
    lut = lut*3 # need one set of data for each band for RGB
    im = im.point(lut)
    return im
    
#~  _____ _ _        _                 _    __                   
#~ |  ___(_) | ___  | | ___   __ _  __| |  / /__  __ ___   _____ 
#~ | |_  | | |/ _ \ | |/ _ \ / _` |/ _` | / / __|/ _` \ \ / / _ \
#~ |  _| | | |  __/ | | (_) | (_| | (_| |/ /\__ \ (_| |\ V /  __/
#~ |_|   |_|_|\___| |_|\___/ \__,_|\__,_/_/ |___/\__,_| \_/ \___|
#~                                                               
    
def save_file_as_dialog(parent, fname, filters = []):
    fc = Gtk.FileChooserDialog(
                parent = parent,
                local_only = True,
                buttons = ("Cancelar", Gtk.ResponseType.CANCEL,
                           "Aceptar",  Gtk.ResponseType.ACCEPT),
                action = Gtk.FileChooserAction.SAVE)
                
    fc.set_current_folder(getcwd())
    fc.set_filename(fname)

    for filt_patterns, filt_name in filters:
        filter = Gtk.FileFilter()
        filter.set_name(filt_name)
        for pattern in filt_patterns.split("|"):
            filter.add_pattern(pattern)
        fc.add_filter(filter)
                
    if fc.run() == Gtk.ResponseType.ACCEPT:
        ret = fc.get_filename()
    else:
        ret = None
    fc.destroy()
    
    return ret


def load_file_dialog(parent, fname, filters):
    fc = Gtk.FileChooserDialog(
                parent = parent,
                local_only = True,
                buttons = ("Cancelar", Gtk.ResponseType.CANCEL,
                           "Aceptar",  Gtk.ResponseType.ACCEPT),
                action = Gtk.FileChooserAction.OPEN)

    fc.set_current_folder(getcwd())

    for filt_patterns, filt_name in filters:
        filter = Gtk.FileFilter()
        filter.set_name(filt_name)
        for pattern in filt_patterns.split("|"):
            filter.add_pattern(pattern)
        fc.add_filter(filter)
                
    if fc.run() == Gtk.ResponseType.ACCEPT:
        ret = fc.get_filename()
    else:
        ret = None
    fc.destroy()
    
    return ret
    


class Test_configuration(Gtk.Grid):
    def __init__(self, parent):
        super(Test_configuration, self).__init__(
                    column_spacing = 8,
                    margin = 6)
        self.conf = Configuration(parent)
        self.conf.load_configuration("config.xml")
        
        self.get_val_path = Gtk.Entry()
        self.get_val_path.connect("activate", self.on_val_activated)
        self.get_val_par  = Gtk.Entry()
        self.get_val_par.connect("activate", self.on_val_activated)
        self.get_el_path = Gtk.Entry()
        self.get_el_path.connect("activate", self.on_el_activated)
        self.get_els_path = Gtk.Entry()
        self.get_els_path.connect("activate", self.on_els_activated)
        
        self.attach(Gtk.Label("Test get_value:", xalign = 1),        0, 0, 1, 1)
        self.attach(Gtk.Label("Path:", xalign = 1),                  1, 0, 1, 1)
        self.attach(self.get_val_path,                               2, 0, 1, 1)
        self.attach(Gtk.Label("Parameter:", xalign = 1),             3, 0, 1, 1)
        self.attach(self.get_val_par,                                4, 0, 1, 1)
        self.attach(Gtk.Label("Test get_element:", xalign = 1),      0, 1, 1, 1)
        self.attach(Gtk.Label("Path:", xalign = 1),                  1, 1, 1, 1)
        self.attach(self.get_el_path,                                2, 1, 1, 1)
        self.attach(Gtk.Label("Test get_all_elements:", xalign = 1), 0, 2, 1, 1)
        self.attach(Gtk.Label("Path:", xalign = 1),                  1, 2, 1, 1)
        self.attach(self.get_els_path,                               2, 2, 1, 1)

        self.bff = Gtk.TextBuffer()
        self.view = Gtk.TextView(buffer = self.bff)

        self.attach(self.view,                                       0, 3, 5, 1)

        
    def on_val_activated(self, entry):
        value = self.conf.get_value(
                    self.get_val_path.get_text(),
                    self.get_val_par.get_text())
        self.bff.insert(self.bff.get_end_iter(), "Value:" + value + "\n")

    def on_el_activated(self, entry):
        value = self.conf.get_element(
                    self.get_el_path.get_text())
        self.bff.insert(self.bff.get_end_iter(), "Element:" + str(list(value)) + "\n")

    def on_els_activated(self, entry):
        value = self.conf.get_all_elements(
                    self.get_els_path.get_text())
        self.bff.insert(self.bff.get_end_iter(), "Elements:" + str(value) + "\n")

#~  __  __       _                                      
#~ |  \/  | __ _(_)_ __      _ __ ___   ___ _ __  _   _ 
#~ | |\/| |/ _` | | '_ \    | '_ ` _ \ / _ \ '_ \| | | |
#~ | |  | | (_| | | | | |   | | | | | |  __/ | | | |_| |
#~ |_|  |_|\__,_|_|_| |_|___|_| |_| |_|\___|_| |_|\__,_|
#~                     |_____|                          

class Main_menu(Gtk.MenuBar):
    def __init__(self, items = []):
        super(Main_menu, self).__init__()
        self.main_menu = {}

        for item in items:
            mitem = Gtk.MenuItem(item)
            self.main_menu[item] = Gtk.Menu()
            mitem.set_submenu(self.main_menu[item])
            self.add(mitem)

            
    def add_items_to(self, main_item, items):
        for (item, handler) in reversed(items):
            if item == None:
                it = Gtk.SeparatorMenuItem()
            else:
                it = Gtk.ImageMenuItem(item)
                it.connect("activate", handler)

            self.main_menu[main_item].insert(it, 0)
            


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 300)

        self.add(Test_configuration(self))

        self.show_all()

    def run(self):
        Gtk.main()


def main(args):
    
    mainwdw = MainWindow()
    mainwdw.run()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
