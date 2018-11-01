#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  rt_math.py
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

import math as m
from copy import deepcopy
from colors import Colors

#~  ____   ____ ____  
#~ |  _ \ / ___| __ ) 
#~ | |_) | |  _|  _ \ 
#~ |  _ <| |_| | |_) |
#~ |_| \_\\____|____/ 
#~

class RGB():
    """ Color: Los compoentes r, g, b estan representado internamente en el
        rango de 0 a 1 (valores punto flotante).

        RGB acepta los siguientes formatos:

            RGB(0.11, 0.22, 0.33)
            RGB((11, 22, 33))
            RGB([11, 22, 33])
            RGB("0.123, 0.233, 0.87")
            RGB("ColorName")
            RGB("#RGB")
            RGB("#RRGGBB")
            RGB("#RRRRGGGGBBBB")
    """
    def __init__(self, r, g = 0, b = 0):
        if isinstance(r, tuple) or isinstance(r, list):
            if len(r) == 3:
                self.r, self.g, self.b = r
            else:
                print("Error in color")
                exit(1)
                
        elif isinstance(r, str):
            if r[0] == '#':
                if len(r) == 4:
                    self.r = int(r[1], 16) / 16
                    self.g = int(r[2], 16) / 16
                    self.b = int(r[3], 16) / 16
                    
                elif len(r) == 7:
                    self.r = int(r[1:3], 16) / 256
                    self.g = int(r[3:5], 16) / 256
                    self.b = int(r[5:7], 16) / 256
                    
                elif len(r) == 13:
                    self.r = int(r[1: 5], 16) / 65536
                    self.g = int(r[5: 9], 16) / 65536
                    self.b = int(r[9:13], 16) / 65536
                
            elif r in Colors:
                self.r, self.g, self.b = Colors[r]
            
            else:
                self.r, self.g, self.b = [float(col) for col in r.split(",")]
                
        else:
            self.r, self.g, self.b = r, g, b


    def __str__(self):
        return "{:g}, {:g}, {:g}".format(self.r, self.g, self.b)


    def __repr__(self):
        return "RGB({:g}, {:g}, {:g})".format(self.r, self.g, self.b)


    def __mul__(self, fact):
        if type(fact) is RGB:
            return RGB(self.r * fact.r,
                       self.g * fact.g,
                       self.b * fact.b)
        else:
            return RGB(self.r * fact,
                       self.g * fact,
                       self.b * fact)

    def __add__(self, rgb1):
        return RGB(self.r + rgb1.r,
                   self.g + rgb1.g,
                   self.b + rgb1.b)


    def limit(self):
        self.r = min(1.0, self.r)
        self.g = min(1.0, self.g)
        self.b = min(1.0, self.b)
        return self
        
         

    def as_percentages(self):
        """ Retorna al color como texto, representando los tres colores
            en el rango de 0 a 100%
        """
        return "rgb({:.0f}%, {:.0f}%, {:.0f}%)".format(
                    min(self.r * 100, 100),
                    min(self.g * 100, 100),
                    min(self.b * 100, 100))


    def as_bytes(self):
        """ Retorna al color como texto, representando los tres colores
            en el rango de 0-255
        """
        return "rgb({:.0f}, {:.0f}, {:.0f})".format(
                    min(self.r * 255, 255),
                    min(self.g * 255, 255),
                    min(self.b * 255, 255))


    def as_byte_tuple(self):
        """ Retorna al color como una tupla de valores de 0-255 (r, g, b)
        """
        return (round(min(self.r * 255, 255)),
                round(min(self.g * 255, 255)),
                round(min(self.b * 255, 255)))


#~ __     _______ ____ _____ 
#~ \ \   / / ____/ ___|___ / 
#~  \ \ / /|  _|| |     |_ \ 
#~   \ V / | |__| |___ ___) |
#~    \_/  |_____\____|____/ 
#~

class VEC3():
    def __init__(self, x, y = 0, z = 0):
        if isinstance(x, tuple) or isinstance(x, list):
            if len(x) == 3:
                self.x, self.y, self.z = x
            else:
                print("Error in vector")
                exit(1)
        elif isinstance(x, str):
            self.x, self.y, self.z = [float(vec) for vec in x.split(",")]
        else:
            self.x, self.y, self.z = x, y, z


    def __str__(self):
        return "{:g}, {:g}, {:g}".format(self.x, self.y, self.z)


    def __repr__(self):
        return "VEC3({:g}, {:g}, {:g})".format(self.x, self.y, self.z)


    def __sub__(self, vec2):
        """ Resta <vec2> de <self> y retorna un nuevo vector
        """
        return VEC3(self.x - vec2.x,
                    self.y - vec2.y,
                    self.z - vec2.z)

    def __add__(self, vec2):
        """ Suma <vec2> a <self> y retorna un nuevo vector
        """
        return VEC3(self.x + vec2.x,
                    self.y + vec2.y,
                    self.z + vec2.z)

    def __mul__(self, fact):
        """ Multiplica <self> con fact. Si <fact> es un VEC3, realiza el
            producto escalar ('dot'), sino multiplica los componentes x, y, z
            con <fact>
        """
        if type(fact) is VEC3:
            return (self.x * fact.x +
                    self.y * fact.y +
                    self.z * fact.z)
        else:
            return VEC3(self.x * fact, self.y * fact, self.z * fact)

    def __abs__(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
        

    def mag(self):
        return m.sqrt(self.x**2 + self.y**2 + self.z**2)
        
        
    def normalize(self):
        """ Normalize <self>, and save the result in <self>
        """
        den = abs(self)
        self.x, self.y, self.z = self.x/den, self.y/den, self.z/den

        return self


    def normalized(self):
        """ Normalize <self>, and return the result as new vector
        """
        den = self.mag()
        return VEC3(self.x/den, self.y/den, self.z/den)

        
    def cross(self, vec2):
        """ Producto vectorial ('cruz') entre <self> y <vec2>
            Retorna un nuevo VEC3
        """
        return VEC3(self.y*vec2.z - self.z*vec2.y,
                    self.z*vec2.x - self.x*vec2.z,
                    self.x*vec2.y - self.y*vec2.x)
                    
                    
    def reflect(self, normal):
        """ Reflect the <self> vector against the <normal> and return the
            reflection.
        """
        spot = self * normal
        return normal * spot * 2 - self
        

    def copy(self):
        return deepcopy(self)

#~ __     _______ ____ _  _   
#~ \ \   / / ____/ ___| || |  
#~  \ \ / /|  _|| |   | || |_ 
#~   \ V / | |__| |___|__   _|
#~    \_/  |_____\____|  |_|

class VEC4():
    def __init__(self, x, y = 0, z = 0, w = 0):
        if isinstance(x, tuple) or isinstance(x, list):
            if len(x) == 3:
                self.x, self.y, self.z = x
            elif len(x) == 4:
                self.x, self.y, self.z, self.w = x
            else:
                print("Error in vector")
                exit(1)
        elif isinstance(x, str):
            self.x, self.y, self.z, self.w = [float(vec) for vec in x.split(",")]
        else:
            self.x, self.y, self.z, self.w = x, y, z, w


    def __str__(self):
        return "{:g}, {:g}, {:g}, {:g}".format(self.x, self.y, self.z, self.w)

                           

#~  __  __    _  _____ _  _   
#~ |  \/  |  / \|_   _| || |  
#~ | |\/| | / _ \ | | | || |_ 
#~ | |  | |/ ___ \| | |__   _|
#~ |_|  |_/_/   \_\_|    |_|  
                           
class MAT4():
    def __init__(self):
        """ Representacion de una matriz de 4x4 elementos
        """
        self.clear()


    def __str__(self):
        s = ""
        for r in range(0, 16, 4):
            s += "{:15g}  {:15g}  {:15g}  {:15g}\n".format(*[self.mat[el] for el in range(r, r+4)])
        return s


    def __mul__(self, v4):
        m4 = self.mat
        return VEC4(
            m4[0]*v4.x   + m4[1]*v4.y   + m4[2]*v4.z   + m4[3]*v4.w,
            m4[4]*v4.x   + m4[5]*v4.y   + m4[6]*v4.z   + m4[7]*v4.w,
            m4[8]*v4.x   + m4[9]*v4.y   + m4[10]*v4.z  + m4[11]*v4.w,
            m4[12]*v4.x  + m4[13]*v4.y  + m4[14]*v4.z  + m4[15]*v4.w)


    def transpose(self):
        m = self.mat
        self.mat = [
            m[0],   m[4],   m[8],   m[12],
            m[1],   m[5],   m[9],   m[13],
            m[2],   m[6],   m[10],  m[14],
            m[3],   m[7],   m[11],  m[15] ]

        
    def clear(self):
        self.mat = [0] * 16


    def set_identity(self):
        self.clear()
        for n in range(0, 16, 5):
            self.mat[n] = 1.0
        return self


    def translation_matrix(self, dx, dy, dz):
        self.set_identity()
        self.mat[3] = dx
        self.mat[7] = dy
        self.mat[11] = dz
        return self

            
    def scale_matrix(self, sx, sy, sz):
        self.set_identity()
        self.mat[0] = sx
        self.mat[5] = sy
        self.mat[10] = sz
        return self

            
    def x_shear_matrix(self, a, b):
        self.set_identity()
        self.mat[4] = a
        self.mat[8] = b
        return self

            
    def y_shear_matrix(self, a, b):
        self.set_identity()
        self.mat[1] = a
        self.mat[9] = b
        return self

            
    def z_shear_matrix(self, a, b):
        self.set_identity()
        self.mat[2] = a
        self.mat[6] = b
        return self

            
    def x_rotation_matrix(self, ang):
        ct = m.cos(ang); st = m.sin(ang)
        self.mat = [
            1,      0,      0,      0,
            0,     ct,    -st,      0,
            0,     st,     ct,      0,
            0,      0,      0,      1 ]
        return self

            
    def y_rotation_matrix(self, ang):
        ct = m.cos(ang)
        st = m.sin(ang)
        self.mat = [
           ct,      0,     st,      0,
            0,      1,      0,      0,
          -st,      0,     ct,      0,
            0,      0,      0,      1 ]
        return self

            
    def z_rotation_matrix(self, ang):
        ct = m.cos(ang)
        st = m.sin(ang)
        self.mat = [
           ct,    -st,      0,      0,
           st,     ct,      0,      0,
            0,      0,      0,      0,
            0,      0,      0,      1 ]
        return self

            
    def copy(self):
        return deepcopy(self)

#~  ____             
#~ |  _ \ __ _ _   _ 
#~ | |_) / _` | | | |
#~ |  _ < (_| | |_| |
#~ |_| \_\__,_|\__, |
#~             |___/ 
        
class Ray():
    """ Los rayos se producen como intancias de Ray, con los siguientes datos:
        loc:  Origen del rayo (= normalment la ubicacion de la camara)
        dir:  Vector de direccion del rayo
    """
    def __init__(self, loc, dir):
        self.loc = loc
        self.dir = dir
        
        
    def __str__(self):
        return "Ray: (Loc: {:s}, Dir: {:s})".format(str(self.loc), str(self.dir))
        
    
    def __repr__(self):
        return "Ray(loc = VEC3({:s}), dir = VEC3({:s}))".format(
                    str(self.loc), str(self.dir))
        
    
    def at(self, t):
        return self.loc + self.dir * t

#~  _   _ _ _   
#~ | | | (_) |_ 
#~ | |_| | | __|
#~ |  _  | | |_ 
#~ |_| |_|_|\__|
#~

class Hit():
    """ Cada impacto se almacena como una instancia de Hit. Los datos a
        guardar son:
            root        El valor de 't' (distancia del origen del rayo)
            normal      La normal en el punto de impacto
            thing       Referencia al elemento en el cual se impactó
    """
    def __init__(self, root, normal, thing):
        self.root = root
        self.normal = normal
        self.thing = thing
        
#~  _____         _      __                  _   _                 
#~ |_   _|__  ___| |_   / _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
#~   | |/ _ \/ __| __| | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#~   | |  __/\__ \ |_  |  _| |_| | | | | (__| |_| | (_) | | | \__ \
#~   |_|\___||___/\__| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#~                                                                 
   
def test_RGB():
    for color in ("12, 23, 34", "21,43,54", "0.54, 0.14, 0.1",
                  "#4080c0", "#48c", "#40008000c000", "CadetBlue"):
        print('RGB("{}") -> '.format(color), RGB(color))
        print(RGB(color).as_percentages())
        
    for color in ((1, 2, 3), [4, 3, 2]):
        print('RGB({}) -> '.format(color), RGB(color))

    for color in ((0.1, 0.2, 0.3), [4, 3, 2]):
        print('RGB({}.as_byte_tuple()) -> '.format(color), RGB(color).as_byte_tuple())
        print('RGB({}.as_bytes()) -> '.format(color), RGB(color).as_bytes())
        print('RGB({}.as_percentages()) -> {}'.format(color, RGB(color).as_percentages()))
        

def test_VEC3():
    for vec in ("12, 23, 34", "21,43,54",
                  (1, 2, 3), [4, 3, 2]):
        v = VEC3(vec)
        vn = v.copy().normalize()
        print(vec, "->", VEC3(vec), "->", vn, "normalized")
    print("1, 2, 3 ->", VEC3(1, 2, 3))
    print("0x11, 0x22, 0x33 ->", VEC3(0x11, 0x22, 0x33))
    
    v1 = VEC3(2, 3, 4)
    v2 = VEC3(5, 6, 7)
    print(v1, "-", v2, " -> ", v1 - v2)

    
def test_products():
    v1 = VEC3(2, 3, 4)
    v2 = VEC3(5, 6, 7)
    print(v1, "cross", v2, " -> ", v1.cross(v2))

    v1 = VEC3(9, 2, 7)
    v2 = VEC3(4, 8, 10)
    print(v1, "*", v2, " -> ", v1 * v2)
   

def test_MAT4():
    for caption, test in (
                ("Creacion matriz",          MAT4()),
                ("Creacion matriz unidad",   MAT4().set_identity()),
                ("Matriz traslacion",        MAT4().translation_matrix(VEC3(22, 33, 44))),
                ("Matriz rotacion en X",     MAT4().x_rotation_matrix(m.radians(30))),
                ("Matriz rotacion en Y",     MAT4().y_rotation_matrix(m.radians(30))),
                ("Matriz rotacion en Z",     MAT4().z_rotation_matrix(m.radians(30))),
                ("Unitario * (7,8,9,1)",     MAT4().set_identity() * VEC4(7,8,9,1))):
        print(caption)
        print(test)


def test_transform():
    for vec4 in (VEC4(1, 0, 0, 1), VEC4(0, 1, 0, 1), VEC4(0, 0, 1, 1)):
        print("Rotating {}".format(vec4))
        print(MAT4().translation_matrix(1, 0, 0) * vec4)
        print(MAT4().translation_matrix(0, 1, 0) * vec4)
        print(MAT4().translation_matrix(0, 0, 1) * vec4)
        print(MAT4().x_rotation_matrix(m.radians(30)) * vec4)
        print(MAT4().y_rotation_matrix(m.radians(30)) * vec4)
        print(MAT4().z_rotation_matrix(m.radians(30)) * vec4)
        print(MAT4().scale_matrix(2, 3, 4) * vec4)

    

    
def test_ray():
    ray = Ray(VEC3(2, 3, 4), VEC3(9, 2, 7))
    print(ray)


def test_reflection():
    v = VEC3(1, 1, 1).normalize()
    for n in ((1, 0, 0), (0, 1, 0), (0, 0, 1),
              (1, 1, 0), (0, 1, 1), (1, 0, 1),
              (1, 1, 1)):
        print("Reflexion de {} con {}: {}".format(v, n, v.reflect(VEC3(n).normalize())))


def main(args):
    #~ test_RGB()
    #~ test_VEC3()
    #~ test_MAT4()
    test_transform()
    #~ test_ray()
    #~ test_products()
    #~ test_reflection()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
