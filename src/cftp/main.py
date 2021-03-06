# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Draw a Random Lozenge Tiling Generated by CFTP with Cairo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage:
    python main.py
"""
import cairocffi as cairo
from cftp import LozengeTiling


TOP_COLOR = (1, 0, 0)
LEFT_COLOR = (0, 1, 1)
RIGHT_COLOR = (0.75, 0.5, 0.25)
EDGE_COLOR = (0, 0, 0)
LINE_WIDTH = 0.1
SQRT3 = 3**0.5

colors = [LEFT_COLOR, RIGHT_COLOR, TOP_COLOR]


def square_to_hex(verts):
    """Transform vertices in square grid to vertices in hexagon grid."""
    return [(SQRT3/2*x, y-0.5*x) for x, y in verts]


def draw(ctx, T):
    """
    ctx: a Cairo context instance.
    T: an instance of `LozengeTiing` class.
    """
    for i, faces in enumerate(T.tiles()):
        for verts in faces:
            A, B, C, D = square_to_hex(verts)
            ctx.move_to(A[0], A[1])
            ctx.line_to(B[0], B[1])
            ctx.line_to(C[0], C[1])
            ctx.line_to(D[0], D[1])
            ctx.close_path()
            ctx.set_source_rgb(*colors[i])
            ctx.fill_preserve()
            ctx.set_line_width(LINE_WIDTH)
            ctx.set_source_rgb(*EDGE_COLOR)
            ctx.stroke()


def main(hexagonsize, imgsize):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, imgsize, imgsize)
    ctx = cairo.Context(surface)

    # we will put the center of the hexagon at the origin
    a, b, c = hexagonsize
    ctx.translate(imgsize/2.0, imgsize/2.0)
    extent = max(c, a*SQRT3/2, b*SQRT3/2) + 1
    ctx.scale(imgsize/(extent*2.0), -imgsize/(extent*2.0))
    ctx.translate(-b*SQRT3/2, -c/2.0)

    # paint background
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()

    T = LozengeTiling(hexagonsize).run_cftp()
    draw(ctx, T)
    surface.write_to_png("random_lozenge_tiling.png")


if __name__ == "__main__":
    main((20, 20, 20), 600)
