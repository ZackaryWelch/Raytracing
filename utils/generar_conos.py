#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  generar_esferas.py
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

from colors import Colors

def generate_conos():
    """ Fabrica una imagen de los 140 colores del archivo colors.py,
        aplicados a esferas. Las esferas estan ubicados en un arreglo de
        4 por 3 unidades, y estan ordenados en 10 filas de 14 esferas.
        Al inicio del 'with open(...' hay algunas lineas que se pueden
        (des)comentar para modificar el comportamiento.
    """
    SCENE_NAME = "140_conos.xml"
    dist = 4.5;                     # Distancia del origen
    radius = 0.13                   # Radio de la esferas
    cone_height = 0.13
    width = 4; height = 3;          # Tamanio del arreglo
    el_hor = 14                     # 14 esferas por fila...
    el_vert = 10                    # y 10 filas
    row_height = height/el_vert
    col_width  = width/el_hor

    color_gen = iter(Colors.values())

    with open(SCENE_NAME, "w") as xmlf:
        #~ render = 'x0="330" x1="470" y0="230" y1="370" '
        render = ''
        
        phong = 'phong="8" '
        #~ phong = ''

        # Introduccion
        print('<scene>\n'
              '  <globals>\n'
              '    <Ambient antialias="0.3" light="0.1, 0.1, 0.1"/>\n'
              '    <Image width="800" height="600" bgcolor="Black" {}/>\n'
              '  </globals>\n'
              '  <lights>\n'
              '    <Point_light reference="light1" location="-1.6, 0.5, 2" color="0.55, 0.55, 0.5" />\n'
              '    <Point_light reference="light2" location="1.6, -0.5, 2" color="0.35, 0.35, 0.35" />\n'
              '  </lights>\n'
              '  <cameras>\n'
              '    <Perspective_cam reference="camera1" location="0, 0, 0" look_at="0, 0, 1" h_angle="48"/>\n'
              '  </cameras>\n'
              '  <things>'.format(render), file = xmlf)

        # Las esferas
        for iy in range(el_vert):
            y0 = row_height * (iy - el_vert/2 + 0.5)

            for ix in range(14):
                x0 = col_width * (ix - el_hor/2 + 0.5)
                
                print('    <Cone reference="{}" center="{}" radius="{}" height="{}" color="{}, {}, {}" {}/>'.format(
                            "cone{}_{}".format(iy, ix),
                            "{}, {}, {}".format(x0, y0, dist),
                            radius,
                            cone_height,
                            *next(color_gen),
                            phong), file = xmlf)

        # ... y el final
        print('  </things>\n'
              '</scene>\n', file = xmlf)
        

def main(args):
    generate_conos()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
