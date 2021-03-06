#!/usr/bin/env python3

# Lenticular interlacer
# Author: Alexander Sheremet <asheremet@gmail.com>
# License: public domain

from PIL import Image
from math import *


def mix_color_component(a, b, proportion):
    """
    @param a, b - color components to mix
    @param proportion - 0-255.
    @return mix
    """
    return (b * proportion + a * (255 - proportion)) // 255


def mix_color(color_a, color_b, proportion):
    component_couples_to_mix = zip(color_a, color_b)
    mixed_components = (mix_color_component(a, b, proportion)
                           for (a,b) in component_couples_to_mix)
    return tuple(mixed_components)


def interlace(nlens, images, height, width):
    image_mode = images[0].mode
    target_image = Image.new(image_mode, (width, height))

    img1 = images[0]
    xx1 = 0
    for x_dest in range(width):
        lens_pos = x_dest * nlens / width

        img_selector = modf(lens_pos)[0] * (len(images))
        img2 = images[trunc(img_selector)]
        xx2 = img2.size[0] * x_dest / width

        proportion = int(modf(img_selector)[0]*255)

        for y_dest in range(height):
            yy1 = img1.size[1] * y_dest // height
            yy2 = img2.size[1] * y_dest // height

            pix1 = img1.getpixel((xx1, yy1))
            pix2 = img2.getpixel((xx2, yy2))

            pix = mix_color(pix1, pix2, proportion)
            target_image.putpixel((x_dest, y_dest), pix)

        img1 = img2
        xx1 = xx2

    return target_image


if __name__ == '__main__':
    import optparse

    usage = "Usage: %prog options {list of source images}"

    parser = optparse.OptionParser(usage)
    parser.add_option("-o", dest="ofile",
                      help="write resulting image to FILE", metavar="FILE")
    parser.add_option("-t", dest="height", type='int',
                      help="height of resulting image in pixels", metavar="HEIGHT")
    parser.add_option("-w", dest="width", type='int',
                      help="width of resulting image in pixels", metavar="FILE")
    parser.add_option("-n", dest="nlens", type='int',
                      help="number of lenticulas on top of image", metavar="LENS_NUMBER")
    parser.add_option("-r", "--dpi", dest="dpi",
                      help="x and y print resolutions (dpi)", metavar="(x_res,y_res)")

    (options, args) = parser.parse_args()

    images = [Image.open(file_name) for file_name in args]

    interlaced_image = interlace(options.nlens, images, height=options.height, width=options.width)

    interlaced_image.save(options.ofile, dpi=eval(options.dpi))

