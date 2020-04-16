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
SIDE_THICKNESS = 1
CORNER_RADIUS = 2
FONT_SIZE = 5

def chopped_cube(size):
    sphr1 = sphere(d=size*1.5)
    sphr2 = sphere(d=size*2)
    sphr = sphr2-sphr1
    c = cube(size, center=True)
    return c-sphr

def create_socket(diameter, z, socket_type):
    s = cylinder(r=diameter/2, h=z)
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

def create_base(size, socket_name, font_size):
    base = union()(
        translate([0, -font_size/2, 0])(cube(size=size, center=True)),
        translate([0, -(1+size[1]/2), size[2]/2])(linear_extrude(1)(text(socket_name, size=font_size, halign="center", valign="bottom")))
        )
    return base

def create_socket_organizer(sockets, depth, socket_size, font_size):
    # Create the left side of the organizer
    base = create_base((SIDE_THICKNESS, depth, SIDE_HEIGHT+BASE_THICKNESS), "", font_size)
    # Shift so bottom of base is at z=0
    base = up((SIDE_HEIGHT+BASE_THICKNESS)/2)(base)
    # Shift so left side of base is at x=0
    offset = SIDE_THICKNESS/2
    organizer = right(offset)(base)
    offset += SIDE_THICKNESS/2

    # Create the socket holders
    for s in sockets:
        x = s[1]+TOLERANCE+DISTANCE_BETWEEN_SOCKS

        # offset needs to take into account the current and previous bases
        offset += (x/2)

        socket = create_socket(s[1]+TOLERANCE, s[2], socket_size)
        socket = up(BASE_THICKNESS)(socket)

        base = create_base((x, depth, SIDE_HEIGHT+BASE_THICKNESS), s[0], font_size)
        base = up((SIDE_HEIGHT+BASE_THICKNESS)/2)(base)

        organizer += right(offset)(base - socket)

        # offset needs to take into account the current and previous bases
        offset += (x/2)
    
    # Create the right side of the organizer
    base = create_base((SIDE_THICKNESS, depth, SIDE_HEIGHT+BASE_THICKNESS), "", font_size)
    base = up((SIDE_HEIGHT+BASE_THICKNESS)/2)(base)
    offset += SIDE_THICKNESS/2
    organizer += right(offset)(base)
    offset += SIDE_THICKNESS/2

    print(f"Total width: {offset}")

    return intersection() (
        # Round the corners
        translate([offset/2,-font_size/2,(SIDE_HEIGHT+BASE_THICKNESS)/2])(rounded_box((offset, depth, SIDE_HEIGHT+BASE_THICKNESS*1.5), CORNER_RADIUS, sidesonly=True)),
        organizer
    )

def assembly1():
    sockets_3_8 = [
        ("7/8", 29.85, 29.15),
        ("13/16", 27.9, 29.6),
        ("3/4", 25.85, 25.8),
        ("11/16", 23.9, 25.5),
    ]
    return create_socket_organizer(sockets_3_8, sockets_3_8[0][1]+10, "3/8", 5)

def assembly2():
    sockets_3_8 = [
        ("5/8", 21.8, 25.5),
        ("9/16", 19.8, 25.5),
        ("1/2", 17.9, 25.5),
        ("7/16", 17, 25.5),
        ("3/8", 17, 25.5),
        ('->1/4', 16.1, 25.5),
    ]
    return create_socket_organizer(sockets_3_8, sockets_3_8[0][1]+10, "3/8", 5)

def assembly3():
    sockets_3_8 = [
        ("19", 25.9, 25.5),
        ("17", 24.0, 25.5),
        ("16", 21.9, 25.5),
        ("15", 21.8, 25.5),
    ]
    return create_socket_organizer(sockets_3_8, sockets_3_8[0][1]+10, "3/8", 5)

def assembly4():
    sockets_3_8 = [
        ("14", 19.8, 25.5),
        ("13", 18.0, 25.5),
        ("12", 17.0, 25.5),
        ("11", 17.0, 25.5),
        ("10", 17, 25.5),
    ]
    return create_socket_organizer(sockets_3_8, sockets_3_8[0][1]+10, "3/8", 5)

def assembly5():
    sockets_1_4 = [
        ("1/2", 17.3, 20.6),
        ("7/16", 15.9, 20.6),
        ("3/8", 13.9, 20.6),
        ("13/32", 13.9, 20.6),
        ("11/32", 13.9, 20.6),
        ("5/16", 12.0, 20.6),
        ("9/32", 12.0, 20.6),
        ("1/4", 11.6, 20.6),
        ("7/32", 11.6, 20.6),
        ("3/16", 11.6, 20.6),
        ("5/32", 11.6, 20.6),
    ]
    return create_socket_organizer(sockets_1_4, sockets_1_4[0][1]+8, "1/4", 4)

def assembly6():
    sockets_1_4 = [
        ("11", 16.0, 20.6),
        ("10", 13.9, 20.6),
        ("9", 13.9, 20.6),
        ("8", 12.0, 20.6),
        ("7", 11.8, 20.6),
        ("6", 11.6, 20.6),
        ("5.5", 11.6, 20.6),
        ("5", 11.6, 20.6),
        ("4.5", 11.6, 20.6),
        ("4", 11.6, 20.6),
        ("Angle", 14.1, 20.6),
    ]
    return create_socket_organizer(sockets_1_4, sockets_1_4[0][1]+8, "1/4", 4)

if __name__ == '__main__':
    a = assembly6()
    scad_render_to_file(a, file_header=f'$fn = {SEGMENTS};', include_orig_code=True)
