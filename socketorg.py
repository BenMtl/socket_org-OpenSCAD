#! /usr/bin/env python3
from solid import *
from solid.utils import * 
import itertools

SEGMENTS = 48

TOLERANCE = 0.3
DISTANCE_BETWEEN_SOCKS = 0.5
BASE_THICKNESS = 2
SIDE_HEIGHT = 5
TEXT_SIZE = 5

def chopped_cube(size):
    sphr1 = sphere(d=size*1.5)
    sphr2 = sphere(d=size*2)
    sphr = sphr2-sphr1
    c = cube(size, center=True)
    return c-sphr

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
    c = chopped_cube(cube_size-(TOLERANCE/2))
    return s-c

def rounded_box(size, radius, sidesonly=False):
    rot = rot = [ [0,0,0], [90,0,90], [90,90,0] ]
    corners = union()

    if sidesonly:
        for x, y in itertools.product([radius-size[0]/2, -radius+size[0]/2], [radius-size[1]/2, -radius+size[1]/2]):
            corners += translate([x, y, 0])(cylinder(radius, size[2], center=True))
        return union()(
            cube(size=(size[0]-2*radius, size[1], size[2]), center=True),
            cube(size=(size[0], size[1]-2*radius, size[2]), center=True),
            corners
        )
    else:
        for axis in range(3):
            for x, y in itertools.product([radius-size[axis]/2, -radius+size[axis]/2], [radius-size[(axis+1)%3]/2, -radius+size[(axis+1)%3]/2]):
                corners += rotate(rot[axis])(translate([x, y, 0])(cylinder(radius, size[(axis+2)%3]-2*radius, center=True)))
            for x, y, z in itertools.product([radius-size[0]/2, -radius+size[0]/2], [radius-size[1]/2, -radius+size[1]/2], [radius-size[2]/2, -radius+size[2]/2]):
                corners += translate([x, y, z])(sphere(radius))

        return union()(
            cube([size[0], size[1]-radius*2, size[2]-radius*2], center=True),
            cube([size[0]-radius*2, size[1], size[2]-radius*2], center=True),
            cube([size[0]-radius*2, size[1]-radius*2, size[2]], center=True),
            corners
        )

def create_base(width, height, depth, socket_name):
    base = union()(
        translate([0, -height/4, 0])(cube(size=(width, depth, height), center=True)),
        # translate([0, -height/4, 0])(rounded_box((width, depth, height), 1)),
        translate([0, -(1+depth/2), height/2])(linear_extrude(1)(text(socket_name, size=5, halign="center", valign="bottom")))
        )
    return base

def create_socket_organizer(sockets, base_depth):
    base = create_base(DISTANCE_BETWEEN_SOCKS, SIDE_HEIGHT+BASE_THICKNESS, base_depth, "")
    base = up((SIDE_HEIGHT+BASE_THICKNESS)/2)(base)
    offset = DISTANCE_BETWEEN_SOCKS/2
    organizer = right(offset)(base)
    for s in sockets:
        base_width = s[1]+TOLERANCE+DISTANCE_BETWEEN_SOCKS

        # offset needs to take into account the current and previous bases
        offset += (base_width/2)

        socket = create_socket(s[1]+TOLERANCE, s[2], "3/8")
        socket = up(BASE_THICKNESS)(socket)

        base = create_base(base_width, SIDE_HEIGHT+BASE_THICKNESS, base_depth, s[0])
        base = up((SIDE_HEIGHT+BASE_THICKNESS)/2)(base)

        organizer += right(offset)(base - socket)

        # offset needs to take into account the current and previous bases
        offset += (base_width/2)
    
    offset += DISTANCE_BETWEEN_SOCKS/2
    base = create_base(DISTANCE_BETWEEN_SOCKS, SIDE_HEIGHT+BASE_THICKNESS, base_depth, "")
    base = up((SIDE_HEIGHT+BASE_THICKNESS)/2)(base)
    organizer += right(offset)(base)
    offset += DISTANCE_BETWEEN_SOCKS/2

    return intersection() (
        # Round the corners
        translate([offset/2,-(SIDE_HEIGHT+BASE_THICKNESS)/4,(SIDE_HEIGHT+BASE_THICKNESS)/2])(rounded_box((offset, base_depth, SIDE_HEIGHT+BASE_THICKNESS+5), 2, sidesonly=True)),
        organizer
    )
    return organizer

def assembly():
    sockets_3_8 = [
        ("7/8", 29.85, 29.15),
        ("13/16", 27.9, 29.6),
        ("3/4", 25.85, 25.8),
    ]
    return create_socket_organizer(sockets_3_8, sockets_3_8[0][1]+10)

if __name__ == '__main__':
    a = assembly()
    scad_render_to_file(a, file_header=f'$fn = {SEGMENTS};', include_orig_code=True)
