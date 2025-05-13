#!/usr/bin/env python3

import argparse

import fpdf


from draw_apriltags.tag_to_svg import make_tag_svg


def entrypoint():
    parser = argparse.ArgumentParser("make_apriltag_sheet")

    parser.add_argument(
        "--family", default="tag25h9", help="Apriltag tag family to use"
    )

    parser.add_argument("--first-id", default=200)

    parser.add_argument(
        "--size",
        default="2in",
        type=str,
        required=False,
        dest="svg_size",
        help='The size (edge length) of the generated svg such as "20mm" "2in" "20px"',
    )

    parser.add_argument("output", type=str, help="The path to the SVG output file.")

    args = parser.parse_args()

    # Parameters that are currently fixed bu should be args
    tag_rows = 4
    tag_cols = 3

    # Space between tags in inches
    tag_spacing = 0.5

    pdf = fpdf.FPDF(unit="in", format=(8.5, 11))
    pdf.add_page()

    pdf.set_font("Helvetica", size=12)
    # pdf.cell(text="Hello world!")

    tag_size = None

    for row in range(0, tag_rows):
        for col in range(0, tag_cols):
            id = row * tag_cols + col

            svg = fpdf.svg.SVGObject(
                make_tag_svg(id, family=args.family, svg_size=args.svg_size)
            )

            # We pass align_viewbox=False because we want to perform positioning manually
            # after the size transform has been computed.
            width, height, paths = svg.transform_to_page_viewport(
                pdf, align_viewbox=False
            )

            # Initialize tag size
            if tag_size is None:
                array_width = tag_cols * width + (tag_cols - 1) * tag_spacing
                array_height = tag_rows * height + (tag_rows - 1) * tag_spacing

                array_origin = ((pdf.w - array_width) / 2, (pdf.h - array_height) / 2)

            # Calculate the upper left corner
            tag_origin = (
                array_origin[0] + col * (width + tag_spacing),
                array_origin[1] + row * (height + tag_spacing),
            )

            print(tag_origin)

            # translation(
            #                 -width / 2, -height / 2
            #             )

            # note: Tag origin is the upper left of the tag?
            paths.transform = paths.transform @ fpdf.drawing.Transform.translation(
                tag_origin[0], tag_origin[1]
            )

    pdf.output(args.output)
