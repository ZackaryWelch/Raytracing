#!/usr/bin/env python3 # -*- coding: utf-8 -*-
#
#  rt_elem.py
#  
#  Copyright 2018 John Coppens <john@jcoppens.com>
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
from gi.repository import Gtk
from rt_math import *
import pdb

#~  _____ _     _             
#~ |_   _| |__ (_)_ __   __ _ 
#~   | | | '_ \| | '_ \ / _` |
#~   | | | | | | | | | | (_| |
#~   |_| |_| |_|_|_| |_|\__, |
#~                      |___/ 

class Thing():
    def __init__(self, reference):
        self.pars = {"reference": reference}


    def __str__(self):
        return ""
        

    def intersected(self, ray):
        pass



class Sphere(Thing):
    def __init__(self, reference,
                location = "0, 0, 0",
                radius = "1",
                color = "1, 1, 1",
                phong = None):
        super(Sphere, self).__init__(reference)
        self.pars.update(
                    location = VEC3(location),
                    radius = float(radius),
                    color = RGB(color),
                    phong = None if phong is None else float(phong) )


    def __str__(self):
        return ("Sphere(ref: {reference}, location: {location}, "
                "radius: {radius}, color: {color}, phong: {phong})").format(**self.pars)


    def intersected(self, ray):
        """ my_loc      ubicacion dentro de la esfera
            my_radius   radio de la esfera
        """
        my_loc = self.pars["location"]
        my_radius = self.pars["radius"]
        a = 1
        v = ray.loc - my_loc
        b = (ray.dir * v) * 2
        c = v.mag()**2 - my_radius**2
        s = b*b - 4*a*c
    
        if s > 0:
            r1 = (-b - m.sqrt(s))/2
            r2 = (-b + m.sqrt(s))/2
            return [Hit( r1, (ray.at(r1) - my_loc).normalize(), self ),
                    Hit( r2, (ray.at(r2) - my_loc).normalize(), self ) ]

        elif s == 0:
            r = -b/2
            return [Hit( r, (ray.at(r) - my_loc).normalize(), self) ]

        else:
            return []



class Box(Thing):
    def __init__(self, reference,
                corner1 = "-0.5, -0.5, -0.5",
                corner2 = "0.5,  0.5,  0.5",
                color = "1, 1, 1"):
        super(Box, self).__init__(reference)
        self.pars.update(
                    corner1 = VEC3(corner1),
                    corner2 = VEC3(corner2),
                    color = RGB(color))


    def __str__(self):
        return ("Box(ref: {reference}, corner1: {corner1}, "
                "corner2: {corner2}, color = RGB(color))").format(**self.pars)


    def intersected(self, ray):
        return []



class Cylinder(Thing):
    def __init__(self, reference,
                center = "0.0, -0.5, 0.0",
                height = "1.0",
                radius = "0.5",
                closed = "True",
                color = "1, 1, 1"):
        super(Cylinder, self).__init__(reference)
        self.pars.update(
                    center = VEC3(center),
                    height = float(height),
                    radius = float(radius),
                    closed = closed == "True",
                    color = RGB(color))


    def __str__(self):
        return ("Cylinder(ref: {reference}, center: {center}, "
                "height: {height}, radius: {radius}, closed: {closed})"
                "color = RGB(color)").format(**self.pars)


    def intersected(self, ray):
        return []



class Cone(Thing):
    def __init__(self, reference,
                center = VEC3(0.0, -0.5, 0.0),
                color = "1,1,1",
                height = 1.0,
                radius = 0.5,
                closed = True,
                phong = None):
        super(Cone, self).__init__(reference)
        self.pars.update(
                    center = VEC3(center),
                    height = float(height),
                    radius = float(radius),
                    closed = closed == "True",
                    color = RGB(color),
                    phong = None if phong is None else float(phong) )


    def __str__(self):
        return ("Cone(ref: {reference}, center: {center}, height: {height}, "
                "radius: {radius}, closed: {closed}), color = RGB(color), phong: {phong}").format(**self.pars)


    def intersected(self, ray):
        """ my_centro    punto en la cima del cono
            my_height    altura del cono
            my_radius    radio del base
        """
       
        my_centro = self.pars["center"]
        my_radius = self.pars["radius"]
        my_height = self.pars["height"]
        height_v = VEC3(0, my_centro.y, 0).normalize()
        v = ray.loc - my_centro
        theta = m.atan2(my_radius, my_height)
        a = (ray.dir * height_v)**2 - m.cos(theta)**2
        c1 = (ray.dir * height_v)
        c2 = (v * height_v)
        c3 = v*(m.cos(theta)**2)
        c4 = ray.dir * c3
        b = ((c1*c2)-c4)*2
        c = (v*height_v)**2-v*v*m.cos(theta)**2 
        s = b*b - 4*a*c
    
        if s > 0:
            r1 = (-b - m.sqrt(s))/(2*a)
            r2 = (-b + m.sqrt(s))/(2*a)
            height = 0 - my_height
            if ((ray.at(r1) - my_centro) * height_v < 0) and ((ray.at(r1) - my_centro) * height_v > height):
                    return [Hit( r1, (ray.at(r1) - my_centro).normalize(), self ),
                            Hit( r2, (ray.at(r2) - my_centro).normalize(), self ) ]
            else:
                return []

        elif s == 0:
            r = -b/(2*a)
            if rayo_1 < 0:
                return [Hit( r, (ray.at(r) - my_centro).normalize(), self) ]
            else:
                return []

        else:
            return []





class Triangle(Thing):
    def __init__(self, reference,
                 vert1 = "-0.5, -0.5, 0.0",
                 vert2 = "-0.5, -0.8, 0.0",
                 vert3 = "-0.5, -0.2, 0.0",
                 color = "1, 1, 1"):
        super(Triangle, self).__init__(reference)
        self.pars.update(
                    vert1 = VEC3(vert1),
                    vert2 = VEC3(vert2),
                    vert3 = VEC3(vert3),
                    color = RGB(color))


    def __str__(self):
        return ("Triangle(ref: {reference}, ver1: {vert1}, vert2: {vert2}, "
                "vert3: {vert3}, color: {color})").format(**self.pars)


    def intersected(self, ray):
        return []
        
        
                  
class Plane(Thing):
    def __init__(self, reference,
                normal = "-0.5, -0.5, -0.5",
                distance = "5.4",
                color = "1, 1, 1",
                phong = None):
        super(Plane, self).__init__(reference)
        self.pars.update(
                    normal = VEC3(normal),
                    distance = float(distance),
                    color = RGB(color),
                    phong = None if phong is None else float(phong) )


    def __str__(self):
        return ("Plane(ref: {reference}, normal: {normal}, "
                "distance: {distance})").format(**self.pars)


    def intersected(self, ray):
        return []



class Picture(Thing):
    def __init__(self, reference,
                filename,
                width = 4,
                height = 3):
        super(Picture, self).__init__(reference)
        self.pars.update(
                    width = int(width),
                    height = int(height),
                    filename = filename)


    def __str__(self):
        return ("Picture(ref: {reference}, filename: {filename}, "
                "width: {width}, height: {height})").format(**self.pars)


    def intersected(self, ray):
        return []

        
#~  _     _       _     _   
#~ | |   (_) __ _| |__ | |_ 
#~ | |   | |/ _` | '_ \| __|
#~ | |___| | (_| | | | | |_ 
#~ |_____|_|\__, |_| |_|\__|
#~          |___/           

class Light():
    def __init__(self, reference):
        self.pars = {"reference": reference};


    def __str__(self):
        return ""



class Point_light(Light):
    def __init__(self, reference, location, color):
        super(Point_light, self).__init__(reference)
        self.pars.update(
                location = VEC3(location),
                color = RGB(color) )


    def __str__(self):
        return ("Point_light: (ref: {reference}, location: {location}, "
                "color: {color})").format(**self.pars)


class Parallel_light(Light):
    def __init__(self, reference, direction, color):
        super(Parallel_light, self).__init__(reference)
        self.pars.update(
                    direction = VEC3(direction),
                    color = RGB(color) )


    def __str__(self):
        return ("Parallel_light: (ref: {reference}, direction: {direction},"
                " color: {color})").format(**self.pars)

#~   ____                               
#~  / ___|__ _ _ __ ___   ___ _ __ __ _ 
#~ | |   / _` | '_ ` _ \ / _ \ '__/ _` |
#~ | |__| (_| | | | | | |  __/ | | (_| |
#~  \____\__,_|_| |_| |_|\___|_|  \__,_|
#~                                      

class Camera():
    def __init__(self, reference):
        self.pars = {"reference": reference}


    def __str__(self):
        return ""


class Perspective_cam(Camera):
    def __init__(self, reference, location, look_at, h_angle):
        super(Perspective_cam, self).__init__(reference)
        self.pars.update(
                    location = VEC3(location),
                    look_at = VEC3(look_at),
                    h_angle = float(h_angle) )


    def __str__(self):
        return ("Perspective: (ref: {reference}, location: {location}, "
                "look_at: {look_at}, h_angle: {h_angle})").format(**self.pars)


#~   ____ _       _           _     
#~  / ___| | ___ | |__   __ _| |___ 
#~ | |  _| |/ _ \| '_ \ / _` | / __|
#~ | |_| | | (_) | |_) | (_| | \__ \
#~  \____|_|\___/|_.__/ \__,_|_|___/
#~                                  

class Ambient():
    def __init__(self, light = "0.1, 0.1, 0.1", antialias = 0.2):
        self.pars = {"light": RGB(light),
                     "antialias": antialias}


    def __str__(self):
        return ("Ambient: (light: {light}, antialias: {antialias:s})").format(**self.pars)



class Image():
    """ Parametros globales re la imagen a generar
            Param       Defecto         Comentario
            width       360             Ancho de la imagen en pixeles
            height      270             Alta de la imagen en pixeles
            bgcolor     0, 0, 0         Color de fondo
            x0, y0      0, 0            Esquina superior izquierda de subimagen
            x1, y1      width, height   Esquina inferior derecha
    """
    def __init__(self, width = 360, height = 270, bgcolor = "Black",
                       x0 = None, y0 = None, x1 = None, y1 = None):
        self.pars = {"width": width,
                     "height": height,
                     "bgcolor": bgcolor,
                     "x0": x0 if x0 is not None else 0,
                     "y0": y0 if y0 is not None else 0,
                     "x1": x1 if x1 is not None else int(width),
                     "y1": y1 if y1 is not None else int(height)}


    def __str__(self):
        return ("Image: (width: {width}, height: {height}, "
                "bgcolor: {bgcolor}, x0: {x0}, y0: {y0}, "
                "x1: {x1}, y1 = {y1})").format(**self.pars)


#~  _____         _      __                  _   _                 
#~ |_   _|__  ___| |_   / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
#~   | |/ _ \/ __| __| | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#~   | |  __/\__ \ |_  |  _| |_| | | | | (__| |_| | (_) | | | \__ \
#~   |_|\___||___/\__| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#~                                                                 

def basic_tests():
    sphere = Sphere("sphere1", "1, 2, 3", "1.2")
    print(sphere)

    box = Box("box123", "-1, -1, -1", "1, 1, 1")
    print(box)

    cylinder = Cylinder("cyl321", "0, -1, 0", "2", "0.75", "False")
    print(cylinder)

    cone = Cone("cone321", "2, -1, 2", "2", "0.75", "False")
    print(cone)

    plane = Plane("plane8", "0.11, 0.22, 0.33", "3.5")
    print(plane)

    pointl = Point_light("pl001", "0.5, 1.5, 2.5", "1.0, 1.0, 1.0")
    print(pointl)

    parallell = Parallel_light("pl001", "3.5, 4.5, 5.5", "1.0, 1.0, 1.0")
    print(parallell)

    persp = Perspective_cam("cam1", "0, 0, 0", "0, 0, 1", "48.0")
    print(persp)

    triangle = Triangle("tri1",
                        "0.5, 1.5, 2.5", "1.0, 1.0, 1.0", "-0.5, -1.0, 0",
                        "0, 1, 1")
    print(triangle)

    ambient = Ambient("0.1, 0.1, 0.1", "0.4")
    print(ambient)
    
    image = Image("360", "270", "0.5, 0.5, 0.5",
                  "10", "10", "250", "260")
    print(image)

    picture = Picture("pic1", "fake_name.png", 4, 3)
    print(picture)


def test_plane_intersection():
    plane = Plane("pl2", "1, 0, 0", 1.5)
    ray = Ray(VEC3("0, 0, 0"), VEC3("1, 1, 0").normalize())
    hit = plane.intersected(ray)
    print(hit.root, hit.normal)

    plane = Plane("pl1", "1, 1, 0", 0.5)
    ray = Ray(VEC3("0, 0, 0"), VEC3("1, 1, 0").normalize())
    hit = plane.intersected(ray)
    print(hit.root, hit.normal)
    


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 300)

        self.show_all()

    def run(self):
        Gtk.main()


def main(args):
    basic_tests()
    test_plane_intersection()

    return 0
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
