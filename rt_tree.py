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
from lxml import etree

import pdb

from rt_math import RGB, VEC3
from rt_elem import *



def xlate(word):
    return {"Cancel": "Cancelar", "Accept": "Aceptar",         # Botones
            "globals": "globales", "lights": "luces",          # categorias
            "things": "cosas", "cameras": "camaras",
            "add": "agregar", "edit": "Modificar",             # operaciones
            "remove": "remover",
            "kind": "tipo",
            "ambient": "ambiente", "reference": "referencia",  # globales 
            "point": "puntual", "parallel": "parelela",        # luces
            "sphere": "esfera", "box": "caja", "cone": "cono", # cosas
            "cylinder": "cilindro", "torus": "Toroide",
            "perspective": "perspectiva"                       # camaras
           }[word]

#~  ____                         _                 
#~ / ___|  ___ ___ _ __   ___   | |_ _ __ ___  ___ 
#~ \___ \ / __/ _ \ '_ \ / _ \  | __| '__/ _ \/ _ \
#~  ___) | (_|  __/ | | |  __/  | |_| | |  __/  __/
#~ |____/ \___\___|_| |_|\___|___\__|_|  \___|\___|
#~                          |_____|                

class Scene_tree(Gtk.Frame):
    def __init__(self, toplevel, scene = None):
        super(Scene_tree, self).__init__(
                    label = "Escena",
                    margin = 4)
        self.toplevel = toplevel
        self.changed = False
        self.scene = scene

        # Element list tree
        self.store = Gtk.TreeStore(str, str, bool)
        self.view = Gtk.TreeView(
                    model = self.store)
        self.view.connect("button-press-event", self.on_button_pressed)

        # Element list tree - tree column
        renderer = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Items", renderer, text = 0)
        self.view.append_column(col)

        # Element list tree - values
        editable_renderer = Gtk.CellRendererText()
        editable_renderer.connect("edited", self.on_value_edited)
        col = Gtk.TreeViewColumn("Values", editable_renderer)
        col.set_attributes(editable_renderer, text = 1, editable = 2)
        self.view.append_column(col)

        # Insert initial categories
        for cat in ("globals", "lights", "cameras", "things"):
            self.store.append( None, (xlate(cat), "", False) )
        
        scroller = Gtk.ScrolledWindow(
                    hexpand = True,
                    vexpand = True)
        scroller.add(self.view)
        
        self.add(scroller)
        
        if self.scene is not None:
            self.show_scene()


    def on_value_edited(self, renderer, path, new_text):
        self.store[self.store.get_iter(path)][1] = new_text
        self.parse_scene()
        self.changed = True

    
    def on_button_pressed(self, trview, event):
        if event.button != 3:                           # Boton derecho?
            return
            
        p = trview.get_path_at_pos(event.x, event.y)    # Click sobre categoria?
        if p == None:
            return
            
        itr = self.store.get_iter(p[0])

        if itr != None:
            category = self.store.get(itr, 1)[0]
            menu = Gtk.Menu()
            for action in ["add", "edit", "", "remove"]:
                if action == "":
                    mitem = Gtk.SeparatorMenuItem()
                else:
                    mitem = Gtk.MenuItem(xlate(action))
                    mitem.connect("activate", self.on_action_selected,
                                category, action)
                menu.append(mitem)
            menu.show_all()
            menu.popup(None, None, None, None, event.button, event.time)


    def show_scene(self, scene = None):
        if scene is not None:
            self.scene = scene
            
        self.store.clear()

        # For each category
        for (key, item) in scene.items():
            cat_itr = self.store.append(None, (key, "", False))

            # for each element in this category
            for (el_key, el_item) in item.items():
                val_itr = self.store.append(cat_itr, (el_key, "", False))

                # for each value defined in this element
                print("-->", el_key, el_item)
                for (val_key, val_item) in el_item.pars.items():
                    self.store.append(val_itr, (val_key, str(val_item), True))

        self.view.expand_all()


    def parse_scene(self, pretty = True):
        # Creamos una representacion interna nueva para la escena
        scene = {}
        
        # Iterar sobre cada categoria en el self.store (globals, lights, ...)
        treeiter = self.store.get_iter_first()
        while treeiter is not None:
            subiter = self.store.iter_children(treeiter)
            category = self.store[treeiter][0]

            # En cada categoria iterar sobre los elementos definidos
            # i.e. 'pt001', 'cam002', etc.
            scene[category] = {}
            while subiter is not None:
                element = self.store[subiter][0]
                
                # Cada elemento puede tener diferentes atributos (color, location, etc)
                # Aqui hacemos un diccionario de todos los atributos
                scene[category][element] = {}
                valueiter = self.store.iter_children(subiter)
                
                while valueiter is not None:
                    value_key = self.store[valueiter][0]
                    scene[category][element][value_key] = self.store[valueiter][1]

                    valueiter = self.store.iter_next(valueiter)

                # Ahora agregarmos el elemento al XML, con sus atributos
                subiter = self.store.iter_next(subiter)

            # Y seguimos con la proxima categoria
            treeiter = self.store.iter_next(treeiter)

        print(scene)
        self.show_scene(scene)
        return


    def save_scene_as(self, fname):
        """ Save scene as an XML file
        """
        self.store.clear()
        root = etree.Element('scene')
        scene_doc = etree.ElementTree(root)
        
        # For each category
        for (key, item) in self.scene.items():
            cat_el = etree.SubElement(root, key)

            # for each element in this category
            for (el_key, el_item) in item.items():

                # for each value defined in this element
                # Use the class name as tag
                print(el_item.pars)
                etree.SubElement(cat_el,                    # parent
                            el_item.__class__.__name__,     # keyword (location, etc)
                            el_item.pars)

        with open(fname, 'wb') as xmlf:
            scene_doc.write(xmlf, pretty_print = True)


    def load_scene_from(self, fname):
        """ Load scene from <fname> (XML file)
        """
        # Creamos una representacion interna nueva para la escena
        scene = {}
        scene_doc = etree.parse(fname)
        root = scene_doc.getroot()

        # Iter over the categories
        for cat in root.getchildren():
            scene[cat.tag] = {}

            # Iter over the items in each category
            for el in cat.getchildren():
                # Iter over the parameters of each element, and create
                # the elements
                par_dict = dict(el.items())
                if "reference" not in par_dict:
                    if el.tag == "Ambient":
                        scene[cat.tag]["ambient"] = Ambient(**par_dict)
                    elif el.tag == "Image":
                        scene[cat.tag]["image"] = Image(**par_dict)
                else:
                    ref = par_dict["reference"]
                    print(ref, par_dict)
                    scene[cat.tag][ref] = {
                        "Sphere": Sphere,
                        "Cylinder": Cylinder,
                        "Cone": Cone,
                        "Box": Box,
                        "Plane": Plane,
                        "Point_light": Point_light,
                        "Parallel_light": Parallel_light,
                        "Perspective_cam": Perspective_cam}[el.tag](**par_dict)

        self.show_scene(scene)



demo_scene = {
    "globals": {
        #~ "ambient": Ambient(light = "0.1, 0.2, 0.3", antialias = "0.3")
    },
    "lights": {
        "pt001":   Point_light(reference = "pt001", location = "1, 2, 3", color = "0.123, 0.234, 0.345"),
        #~ "par002":  Parallel_light("par002", "1, 2, 3", "0.123, 0.234, 0.345"),
        #~ "par003":  Parallel_light("par003", "2, 3, 4", "0.123, 0.234, 0.345")
    },
    "cameras": {
        #~ "per1":    Perspective_cam("per1", "0, 0, 0", "0, 0, 1", "48.0")
    },
    "things": {
        "sphere1": Sphere("sphere1", "1, 2, 3", "1.0", "0, 0, 1")
    }
}


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(500, 300)

        scene = Scene_tree(self)

        scene.show_scene(demo_scene)
        pdb.set_trace()
        new_scene = scene.parse_scene()
        #~ scene.save_scene_as(demo_scene, "demo.xml")
        #~ new_scene = scene.load_scene_from("demo.xml")
        
        self.add(scene)
        
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
