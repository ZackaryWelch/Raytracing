#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  import_colors.py
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

#~ URL = "http://www.discoveryplayground.com/computer-programming-for-kids/rgb-colors/"
URL = "https://www.w3schools.com/colors/colors_names.asp"

import requests
import re
from bs4 import BeautifulSoup

def extract_colors_playground(page):
    """ La pagina contiene <td>'s con esta estructura:
            <tr>
            <td>Snow 3</td>
            <td>205<a name="PA"></a>-201-201</td>
            <td>cdc9c9</td>
            <td bgcolor="cdc9c9">&nbsp;</td>
            </tr>
    """
    soup = BeautifulSoup(page, 'html.parser')

    col_dict = {}
    for row in soup.find_all("tr"):
        all_td = row.find_all("td")
        if all_td[0].string != "Color Name":
            r = re.search("([0-9a-f]{6})", all_td[2].string)
            if r == None:
                print("No pude decodificar color: ", all_td[0])
            else:
                rgb = r.group(1)
                r = int(rgb[0:2], 16) / 256
                g = int(rgb[2:4], 16) / 256
                b = int(rgb[4:6], 16) / 256
                col_dict[all_td[0].string] = "{:g}, {:g}, {:g}".format(r, g, b)

    return col_dict

def extract_colors_w3schools(page):
    """ La pagina contiene <tr>'s con esta estructura:
            <tr>
            <td><a href="/colors/color_tryit.asp?color=YellowGreen" target="_blank">YellowGreen</a> </td>
            <td><a href="/colors/color_tryit.asp?hex=9ACD32" target="_blank">#9ACD32</a></td>
            <td style="background-color:#9ACD32"> </td>
            <td><a href="/colors/colors_picker.asp?colorhex=9ACD32">Shades</a></td>
            <td><a href="/colors/colors_mixer.asp?colorbottom=9ACD32&amp;colortop=FFFFFF">Mix</a></td>
            </tr>
    """
    soup = BeautifulSoup(page, 'html.parser')

    col_dict = {}
    table = soup.find_all("table")

    for cell in table[0].find_all("tr")[1:]:        # Skip header line
        all_td = cell.find_all("td")

        r = re.search("#([0-9A-F]{6})", all_td[1].string)
        if r == None:
            print("No pude decodificar color: ", all_td[0])
        else:
            rgb = r.group(1)
            r = int(rgb[0:2], 16) / 256
            g = int(rgb[2:4], 16) / 256
            b = int(rgb[4:6], 16) / 256
            col_dict[all_td[0].a.string] = "{:g}, {:g}, {:g}".format(r, g, b)

    return col_dict


def save_coldict(coldict, dict_name, fname):
    with open(fname, "w") as outf:
        outf.write('{} = {{\n'.format(dict_name))
        for key in sorted(coldict.keys()):
            outf.write('    "{:s}": ({:s}),\n'.format(key, coldict[key]))
        outf.write('}')
        

def main(args):
    r = requests.get(URL)
    col_dict = extract_colors_w3schools(r.content)
    save_coldict(col_dict, "Colors", "colors.py")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
