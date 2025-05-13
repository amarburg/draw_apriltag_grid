#!/usr/bin/env python3
#
# Copied from [apriltag-img](https://github.com/AprilRobotics/apriltag-imgs) repo


from PIL import Image
from pathlib import Path


def make_tag_file_name(id, family):
    """ """

    # Check for submodule
    if not (Path("apriltag-imgs") / "tag_to_svg.py").exists():
        raise ValueError(
            "apriltag-imgs/tag_to_svg.py doesn't exist.  Is the submodule checked out?"
        )

    p = Path("apriltag-imgs") / family

    if not p.is_dir():
        raise ValueError(f"Family directory {p} doesn't exist")

    # Family name is part of tag name...
    if family in ["tag16h5", "tag25h9", "tag36h11"]:
        fname = f"{family.replace('h', '_0')}_{id:05d}.png"

        tag_file = p / fname
        if not tag_file.exists():
            raise ValueError(f"Can't find tag file {tag_file}")

    else:
        raise ValueError(f"Can't create file names for family {family}")

    return tag_file


def make_tag_svg(id, family, svg_size):
    tag_file = make_tag_file_name(id, family)

    if tag_file is None:
        raise ValueError("Couldn't find tag file")

    with Image.open(tag_file, "r") as im:
        width, height = im.size
        pix_vals = im.load()

        apriltag_svg = gen_apriltag_svg(width, height, pix_vals, svg_size)

    return apriltag_svg


def gen_apriltag_svg(width, height, pixel_array, size, draw_outline=True):
    def gen_rgba(rbga):
        (_r, _g, _b, _raw_a) = rbga
        _a = _raw_a / 255
        return f"rgb({_r}, {_g}, {_b})"

    # fpdf can't handle rgba?
    #        return f'rgba({_r}, {_g}, {_b}, {_a})'

    def gen_gridsquare(row_num, col_num, pixel):
        _rgba = gen_rgba(pixel)
        _id = f"box{row_num}-{col_num}"
        return f'\t<rect width="1" height="1" x="{row_num}" y="{col_num}" fill="{_rgba}" id="{_id}"/>\n'

    svg_text = '<?xml version="1.0" standalone="yes"?>\n'
    svg_text += f'<svg width="{size}" height="{size}" viewBox="0,0,{width},{height}" xmlns="http://www.w3.org/2000/svg">\n'

    for _y in range(height):
        for _x in range(width):
            svg_text += gen_gridsquare(_x, _y, pixel_array[_x, _y])

    if draw_outline:
        svg_text += f'\t<rect width="{width}" height="{height}" x="0" y="0" fill-opacity="0" stroke="grey" stroke-width="0.1" stroke-dasharray="2 1" stroke-opacity="0.2" />\n'

    svg_text += "</svg>\n"

    return svg_text
