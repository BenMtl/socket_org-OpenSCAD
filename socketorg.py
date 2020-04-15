#! /usr/bin/env python3
from solid import *
from solid.utils import * 

SEGMENTS = 48

TOLERANCE = 0.3
DISTANCE_BETWEEN_SOCKS = 1
BASE_THICKNESS = 5
SIDE_HEIGHT = 5

def create_socket(diameter, height, socket_type):
    s = cylinder(r=diameter/2, h=height)
    if socket_type == "1/4":
        cube_size = 6
    elif socket_type == "3/8":
        cube_size = 9
    elif socket_type == "1/2":
        cube_size = 13
    elif socket_type == "3/4":
        cube_size = 19
    c = cube(cube_size-TOLERANCE, center=True)
    return s-c

def create_base(width, height, socket_name):
    base = union()(
        translate([0, -height/4, 0])(cube(size=(width, 40, height), center=True)),
        translate([0, -22, height/2])(linear_extrude(1)(text(socket_name, size=5, halign="center", valign="bottom")))
        )
    return base

def assembly():
    sockets_3_8 = [
        ("7/8", 29.85, 29.15),
        ("13/16", 27.9, 29.6),
        ("3/4", 25.85, 25.8),
    ]
    offset = 0
    organizer = difference()
    for s in sockets_3_8:
        socket = create_socket(s[1]+TOLERANCE, s[2], "3/8")
        socket = up(BASE_THICKNESS)(socket)

        base_width = s[1]+TOLERANCE+DISTANCE_BETWEEN_SOCKS
        base = create_base(base_width, SIDE_HEIGHT+BASE_THICKNESS, s[0])
        base = up((SIDE_HEIGHT+BASE_THICKNESS)/2)(base)

        unit = base - socket
        unit = right(offset)(unit)
        organizer = organizer + unit
        offset += base_width
    
    return organizer

if __name__ == '__main__':
    a = assembly()
    scad_render_to_file(a, file_header=f'$fn = {SEGMENTS};', include_orig_code=True)
