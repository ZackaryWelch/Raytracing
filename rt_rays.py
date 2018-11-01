#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  rt_rays.py
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
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib, GdkPixbuf

from PIL import Image, ImageColor
from rt_aux import *
from rt_math import VEC3, RGB, Ray
import math as m
import os.path as osp

#~  ____                                               _             
#~ |  _ \ __ _ _   _    __ _  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
#~ | |_) / _` | | | |  / _` |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
#~ |  _ < (_| | |_| | | (_| |  __/ | | |  __/ | | (_| | || (_) | |   
#~ |_| \_\__,_|\__, |  \__, |\___|_| |_|\___|_|  \__,_|\__\___/|_|   
#~             |___/   |___/                                         

class Ray_generator():
    def __init__(self, size_x, size_y, res_x, res_y,
                       loc = VEC3(0, 0, 0), look_at = VEC3(0, 0, 1)):
        """ Generador de rayos (re)simplificado:
            res_x, res_y:	Resolucion horizontal y vertical en pixeles
            size_x, size_y: Tamanio de la 'pantalla' en unidades de
            Retorna:
                Un <Ray> 	Origen (loc): (por defecto es 0, 0, 0)
                            Direccion (dir): se calcula aqui
        """
        self.size = size_x, size_y
        self.res_x = res_x
        self.res_y = res_y
        self.loc = loc
        self.look_at = look_at
        
        
    def generate(self, x0, y0, x1, y1):
        """ Generar los rayos para renderizar la imagen. La imagen generada
            puede ser menor o igual que el tamano definido.
                sub_x0, sub_y0: Esquina superior izquierda
                sub_x1, sub_y1: Esquina inferior derecha
        """
        assert (x0 <= x1) and (y0 < y1)
        assert (x0 >=  0) and (y0 >= 0)
        assert (x1 <= self.res_x) and (y1 <= self.res_y)

        # Para cada fila de pixeles:
        for iy in range(y0, y1):
            y = (self.res_y//2 - 0.5 - iy) / self.res_y*self.size[1]

            # Para cada pixel en la fila
            for ix in range(x0, x1):
                x = (ix - self.res_x//2 + 0.5) / self.res_x*self.size[0]
                yield (Ray(self.loc, VEC3(x, y, 1).normalize()),
                       ix,
                       iy)
            
#~   ____                          
#~  / ___|__ _ _ ____   ____ _ ___ 
#~ | |   / _` | '_ \ \ / / _` / __|
#~ | |__| (_| | | | \ V / (_| \__ \
#~  \____\__,_|_| |_|\_/ \__,_|___/
#~                                 
            
class Canvas(Gtk.Frame):
    def __init__(self):
        super(Canvas, self).__init__(
                    label = "Resultado",
                    margin = 4)
                    
        self.img = Gtk.Image()
        evbox = Gtk.EventBox()
        evbox.add(self.img)
        evbox.connect("button_press_event", self.on_button_pressed)
        
        scroller = Gtk.ScrolledWindow()
        scroller.add(evbox)
        
        self.add(scroller)


    def create_pil_image(self, w, h, bg = "Black"):
        self.img_pil = Image.new("RGB", (w, h), bg)
        self.update_pixbuf()
        
        GLib.timeout_add(500, self.update_pixbuf)


    def update_pixbuf(self):
        self.pxb = image2pixbuf(self.img_pil.copy())
        self.img.set_from_pixbuf(self.pxb)
        return True


    def on_button_pressed(self, img, event):
        if event.button != 3:
            return

        menu = Gtk.Menu()
        mitem = Gtk.MenuItem("Guardar imagen como...")
        mitem.connect("activate", self.on_save_activated)
        menu.append(mitem)
        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)


    def on_save_activated(self, mitem):
        fname = save_file_as_dialog(self.get_toplevel(), "image.png",
                    (("*.png|*.jpeg|*.jpg|*.bmp", "Image files"),
                     ("*", "All files")) )
        if fname == None:
            return

        path, ftype = osp.splitext(fname)
        ftype = "jpeg" if ftype == ".jpg" else ftype[1:]
        self.pxb.savev(fname, ftype, [], [])
        
    
    def fill_color(self, color):
        self.img_pil.paste(
                    color,
                    [0, 0, self.img_pil.size[0],self.img_pil.size[1]])
        
        
    def set_pixel(self, x, y, color):
        self.img_pil.putpixel((x, y), color)

#~  _____                        
#~ |_   _| __ __ _  ___ ___ _ __ 
#~   | || '__/ _` |/ __/ _ \ '__|
#~   | || | | (_| | (_|  __/ |   
#~   |_||_|  \__,_|\___\___|_|   
#~
                              
class Tracer():
    def __init__(self, parent):
        p = self.parent = parent
        psc = p.scenetree.scene

        img_w = int(psc["globals"]["image"].pars["width"])
        img_h = int(psc["globals"]["image"].pars["height"])
        x0 = int(psc["globals"]["image"].pars["x0"])
        y0 = int(psc["globals"]["image"].pars["y0"])
        x1 = int(psc["globals"]["image"].pars["x1"])
        y1 = int(psc["globals"]["image"].pars["y1"])
        
        self.img_aspect  = img_h / img_w
        self.cam_loc = psc["cameras"]["camera1"].pars["location"]
        self.h_angle = psc["cameras"]["camera1"].pars["h_angle"]
        h_size = 2 * m.tan(m.radians(self.h_angle/2))
        
        bgcolor = psc["globals"]["image"].pars["bgcolor"]
        self.ambient = psc["globals"]["ambient"].pars["light"]
        
        p.canvas.create_pil_image(img_w, img_h, bgcolor)
        
        raygen = Ray_generator( h_size, h_size * self.img_aspect,
                                img_w, img_h)
                                
        self.gen = raygen.generate(x0, y0, x1, y1)
    
    
    def find_intersections(self, ray):
        hits = []
        for thing in self.parent.scenetree.scene["things"]:
            o = self.parent.scenetree.scene["things"][thing]
            hits += o.intersected(ray)

        if len(hits) != 0:
            hits.sort(key = lambda x: x.root)
            return hits[0]
        else: 
            return None


    def render(self):
        # Para todos los rayos (pixeles) de la imagen:
        for ray, ix, iy in self.gen:
            
            # Para cada objeto en la escena:
            nearest_hit = self.find_intersections(ray)

            pixel_color = RGB("Black")

            if nearest_hit != None:
                nearest_color = nearest_hit.thing.pars["color"]
                phong = nearest_hit.thing.pars["phong"]
                
                # Ambient color component
                pixel_color = pixel_color + (nearest_color * self.ambient)
                
                for light in self.parent.scenetree.scene["lights"]:
                    l = self.parent.scenetree.scene["lights"][light]
                    lpos = l.pars["location"]
                    lcol = l.pars["color"]
                    
                    # Creamos un rayo desde la fuente de luz hasta el punto
                    # de impacto en el objeto, para determinar si llega la luz
                    lray = Ray(lpos,
                               (ray.at(nearest_hit.root) - lpos).normalize())
                    lhit = self.find_intersections(lray)
                    if lhit is None:
                        continue
                        
                    # Seguro encontraremos una interseccion - pero ocurre entre
                    # la fuente de luz y el objeto?
                    light2hit = (lpos - ray.at(nearest_hit.root)).mag()

                    if (lhit.root - light2hit) > -1e-12:
                        # Angulo entre normal y ray de luz es la intensidad
                        #   La normal es hit.normal
                        #   Rayo de luz es lray.direction
                        cos_ang = -(lhit.normal * lray.dir)
                        diffuse_color = nearest_color * lcol
                        pixel_color = pixel_color + diffuse_color * cos_ang

                        if phong is not None:
                            phong_cos = lray.dir.reflect(lhit.normal) * ray.dir
                            if phong_cos >= 0:
                                phong_cos **= phong
                                pixel_color = pixel_color + lcol * phong_cos


                thing_color = pixel_color.as_byte_tuple()
                #~ print(thing_color)
                self.parent.canvas.set_pixel(ix, iy, thing_color)


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 300)
        
        cv = Canvas()
        self.add(cv)

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
