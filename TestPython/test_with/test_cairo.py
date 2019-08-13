__author__ = 'R.Azh'

import cairo
import math


#  The pycairo drawing library contains a Context class which exposes a
#  save method, to push the current drawing state on an internal stack,
#  and a restore method, to restore the drawing state from the stack.

Width, Height = 280, 204

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, Width, Height)

cr = cairo.Context(surface)

cr.translate(68, 68)
for i in range(6):
    cr.save()
    cr.rotate(2 * math.pi * i / 6)
    cr.rectangle(-25, -60, 50, 40)
    cr.stroke()
    cr.restore()

surface.write_to_png('image.png')

# That’s a fairly simple example, but for larger scripts, it can become
# cumbersome to keep track of which save goes with which restore, and to
#  keep them correctly matched. The with statement can help tidy things up a bit.
#  pycairo’s save and restore methods do not support the with statement,
#  so we’ll have to add the support on our own.

# There are two ways to support the with statement:
#  by implementing a context manager class,
# or by writing a generator function.


#####################################################
#   Implementing the Context Manager as a Class   ###
#####################################################

# To implement a context manager, we define a class containing an __enter__
# and __exit__ method.

# The Saved object is considered to be the context manager.
class Saved():
    def __init__(self, cr):  # cr is a cairo context
        self.cr = cr

    def __enter__(self):
        self.cr.save()
        return self.cr

    def __exit__(self, type, value, traceback):
        self.cr.restore()


for i in range(6):
    with Saved(cr):
        cr.rotate(2 * math.pi * i/6)
        cr.rectangle(-25, -60, 50, 40)
        cr.stroke()
# we have not specified the optional "as" target part of the with statement.
# Therefore, the return value is not saved anywhere. We don’t need it;
#  we know it’s the same cairo context that we passed in.

surface.write_to_png('image.png')

# if an exception occurs: It passes information about the exception in three
# arguments: (type, value, traceback) – the same values you’d get by
# calling sys.exc_info.


#####################################################
#  Implementing the Context Manager as a Generator  #
#####################################################

# Instead of implementing a class for the context manager, we can write a
#  generator function.

from contextlib import  contextmanager


@contextmanager
def saved(cr):
    cr.save()
    yield cr
    cr.restore()
# this example is incomplete, since it does not handle exceptions very well.
# This approach involves many more steps, and a lot more complexity than the
# previous approach.

for i in range(6):
    with saved(cr):
        cr.rotate(2 * math.pi * i/6)
        cr.rectangle(-25, -60, 50, 40)
        cr.stroke()

surface.write_to_png('image.png')

# our current generator function has a problem: if an exception occurs, restore
#  will not be called on the cairo context.
# if An exception has been raised on the line containing the yield statement, so
# the rest of the generator function will not be executed. We need to make
# the generator more robust, by inserting a try/finally block around the yield


@contextmanager
def saved_(cr):
    cr.save()
    try:
        yield cr
    finally:
        cr.restore()


def Tree(angle):
    cr.move_to(0, 0)
    cr.translate(0, -65)
    cr.line_to(0, 0)
    cr.stroke()
    cr.scale(0.72, 0.72)
    if angle > 0.12:
        for a in [-angle, angle]:
            with saved_(cr):
                cr.rotate(a)
                Tree(angle * 0.75)

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 280, 204)
cr = cairo.Context(surf)
cr.translate(140, 203)
cr.set_line_width(5)
Tree(0.75)
surf.write_to_png('fractal-tree.png')
