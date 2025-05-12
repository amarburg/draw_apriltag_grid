#!/usr/bin/env python3

from pathlib import Path
import argparse
import numpy as np

import fpdf


from draw_apriltags.tag_to_svg import make_tag_svg

def entrypoint():

    parser = argparse.ArgumentParser("make_apriltag_sheet")

    parser.add_argument("--family", default="tag25h9", help="Apriltag tag family to use")
    parser.add_argument("--first-id", default=0)

    parser.add_argument(
        'out_file', type=str, 
        help='The path to the SVG output file.'
    )
    parser.add_argument(
        '--size', default="2in", type=str, required=False,  dest="svg_size", 
        help='The size (edge length) of the generated svg such as "20mm" "2in" "20px"'
    )

    args = parser.parse_args()


    tag_rows = 4
    tag_cols = 3

    # Location of origin in meters
    tag_origin = (0,0)

    # Space between tags in meters
    tag_spacing = (0,0)

    total_tags = tag_rows * tag_cols

    tag_ids = np.arange(args.first_id, args.first_id+total_tags)
    print(tag_ids)

    tag_svgs = [make_tag_svg(id, family=args.family, svg_size=args.svg_size) for id in tag_ids]

    pdf = fpdf.FPDF(unit="in", format=(8.5, 11))
    pdf.add_page()
    pdf.set_font('Helvetica', size=12)
    pdf.cell(text="Hello world!")


    for tag_svg in tag_svgs:
        svg = fpdf.svg.SVGObject(tag_svg)
        
        # We pass align_viewbox=False because we want to perform positioning manually
        # after the size transform has been computed.
        width, height, paths = svg.transform_to_page_viewport(pdf, align_viewbox=False)
        # note: transformation order is important! This centers the svg drawing at the
        # origin, rotates it 90 degrees clockwise, and then repositions it to the
        # middle of the output page.
        paths.transform = paths.transform @ fpdf.drawing.Transform.translation(
            -width / 2, -height / 2
        ).rotate_d(90).translate(pdf.w / 2, pdf.h / 2)

        pdf.draw_path(paths)


    pdf.output("hello_world.pdf")