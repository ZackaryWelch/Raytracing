#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  scene_edit.py
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
from gi.repository import Gtk, GooCanvas
from rt_tree import Scene_tree
from rt_aux import Main_menu, load_file_dialog, save_file_as_dialog
from rt_rays import Canvas, Tracer
import pdb

CONFIG_FILE = "config.xml"
VERSION = "0.3"
AUTHORS = ("John Coppens", )
WEBSITE = "http://jcoppens.com"

#~  __  __       _                  _           _               
#~ |  \/  | __ _(_)_ __   __      _(_)_ __   __| | _____      __
#~ | |\/| |/ _` | | '_ \  \ \ /\ / / | '_ \ / _` |/ _ \ \ /\ / /
#~ | |  | | (_| | | | | |  \ V  V /| | | | | (_| | (_) \ V  V / 
#~ |_|  |_|\__,_|_|_| |_|___\_/\_/ |_|_| |_|\__,_|\___/ \_/\_/  
#~                     |_____|                                  

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        
        self.set_size_request(600, 450)
        
        self.scenetree = Scene_tree(self)
        self.canvas = Canvas()
        
        self.main_menu = self.make_main_menu()
        self.nb = Gtk.Notebook()
        self.nb.append_page(self.canvas, Gtk.Label("Canvas"))
        self.nb.append_page(self.scenetree, Gtk.Label("Escena"))
        
        self.render_btn = Gtk.Button("Renderizar")
        self.render_btn.connect("clicked", self.on_render_btn_clicked)

        grid = Gtk.Grid()
        grid.attach(self.main_menu,     0, 0, 1, 1)
        grid.attach(self.nb,            0, 1, 1, 1)
        grid.attach(self.render_btn,    0, 2, 1, 1)

        self.add(grid)
        self.show_all()


    def make_main_menu(self):
        menu = Main_menu( ["Archivo", "Editar", "Ayuda"] )
        menu.add_items_to("Archivo", (
                    ("Cargar escena",  self.on_load_scene),
                    ("Guardar escena como...", self.on_save_scene_as),
                    (None, None),
                    ("Salir",          self.on_quit)))
        menu.add_items_to("Ayuda", (
                    ("Acerca...",  self.on_about), ))
        return menu

        
    def on_render_btn_clicked(self, btn):
        tracer = Tracer(self)
        tracer.render()
        
        
    def on_quit(self, mitem):
        Gtk.main_quit()


    def on_load_scene(self, mitem):
        fname = load_file_dialog(self, "",
                    (("*.xml", "XML files"),
                     ("*", "All files")) )
        if fname != None:
            self.scenetree.load_scene_from(fname)


    def on_save_scene_as(self, mitem):
        fname = save_file_as_dialog(self, "",
                    (("*.xml", "XML files"),
                     ("*", "All files")) )
        if fname != None:
            self.scenetree.parse_scene()
            self.scenetree.save_scene_as(fname)


    def on_about(self, mitem):
        dlg = Gtk.AboutDialog(parent = self.get_toplevel(),
                              version = VERSION,
                              program_name = "rt_main",
                              authors = AUTHORS,
                              license_type = Gtk.License.GPL_3_0)
        dlg.run()
        dlg.destroy()


    def fatal_error_dialog(self, message):
        dlg = Gtk.MessageDialog(
                    parent = self,
                    text = message,
                    buttons = ("Aceptar", Gtk.ResponseType.ACCEPT))
        dlg.run()
        dlg.destroy()
        

    def warning_error_dialog(self, message):
        dlg = Gtk.MessageDialog(
                    parent = self,
                    text = message,
                    buttons = ("Aceptar", Gtk.ResponseType.ACCEPT))
        dlg.run()
        dlg.destroy()
        

    def run(self):
        Gtk.main()



def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
