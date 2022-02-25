#!/usr/bin/env python3

"""
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
"""

import sys
import os

# sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(
    os.path.join(sys.path[0], "..", "..", "..")
)  # load parent path of KicadModTree
from math import sqrt
import argparse
import yaml
from helpers import roundToBase
from KicadModTree import *

sys.path.append(
    os.path.join(sys.path[0], "..", "..", "tools")
)  # load parent path of tools
from footprint_text_fields import addTextFields



series = "Micro-Fit_3.0"
series_long = "Micro-Fit 3.0 Connector System"
manufacturer = "Molex"
orientation = "H"
number_of_rows = 1
datasheet = "https://www.molex.com/pdm_docs/sd/436500210_sd.pdf"

# Molex part number
# n = number of circuits per row
part_code = "43650-{n:02}10"

alternative_codes = [
    "43650-{n:02}11",
    "43650-{n:02}09",
]

variant_params = {
    "hand": {
        "mount_hole_diameter": 2.41,
        "suffix": ""
    },
    "pnp": {
        "mount_hole_diameter": 2.54,
        "suffix": "_PnP"
    },
}

pitch = 3.0
pincount_range = list(range(2, 13))

row = 5.5

pad_size = [1.27, 2.92]


def generate_one_footprint(pins, variant, configuration):
    mpn = part_code.format(n=pins)
    alt_mpn = [code.format(n=pins) for code in alternative_codes]

    # handle arguments
    orientation_str = configuration["orientation_options"][orientation]
    footprint_name = configuration["fp_name_format_string"].format(
        man=manufacturer,
        series=series,
        mpn=mpn,
        num_rows=number_of_rows,
        pins_per_row=pins,
        mounting_pad="-1MP",
        pitch=pitch,
        orientation=orientation_str,
    )
    footprint_name += variant_params[variant]["suffix"]

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(
        "Molex {:s}, {:s} (compatible alternatives: {:s}), {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(
            series_long, mpn, ", ".join(alt_mpn), pins, datasheet
        )
    )
    kicad_mod.setTags(
        configuration["keyword_fp_string"].format(
            series=series,
            orientation=orientation_str,
            man=manufacturer,
            entry=configuration["entry_direction"][orientation],
        )
    )

    kicad_mod.setAttribute("smd")

    # Calculate dimensions
    B = (pins - 1) * pitch

    A = B + 6.65
    C = B + 4.3
    # D = pitch_y + PadSiseY
    pad_row_1_y = 9.90 / 2 + 0.17
    pad1_x = -B / 2

    mount_pad_x = C / 2
    mount_pad_y = pad_row_1_y - (6.93 - pad_size[1] / 2)

    body_edge = {"left": -A / 2, "right": A / 2, "top": mount_pad_y - 4.6}
    body_edge["bottom"] = body_edge["top"] + 9.90

    mount_hole_diameter = variant_params[variant]["mount_hole_diameter"]

    #
    # Add solder nails
    #
    mount_hole_pad_diameter = mount_hole_diameter + 0.3
    kicad_mod.append(
        Pad(
            at=[-mount_pad_x, mount_pad_y],
            number=configuration["mounting_pad_number"],
            type=Pad.TYPE_THT,
            shape=Pad.SHAPE_CIRCLE,
            size=mount_hole_pad_diameter,
            drill=mount_hole_diameter,
            layers=Pad.LAYERS_THT,
        )
    )
    kicad_mod.append(
        Pad(
            at=[mount_pad_x, mount_pad_y],
            number=configuration["mounting_pad_number"],
            type=Pad.TYPE_THT,
            shape=Pad.SHAPE_CIRCLE,
            size=mount_hole_pad_diameter,
            drill=mount_hole_diameter,
            layers=Pad.LAYERS_THT,
        )
    )

    #
    # Add pads
    #
    kicad_mod.append(
        PadArray(
            start=[pad1_x, pad_row_1_y],
            initial=1,
            pincount=pins,
            increment=1,
            x_spacing=pitch,
            size=pad_size,
            type=Pad.TYPE_SMT,
            shape=Pad.SHAPE_RECT,
            layers=Pad.LAYERS_SMT,
        )
    )

    #
    # Add F.Fab, F.SilkS, F.CrtYd
    #
    LineDXA = [
        0,
        configuration["silk_fab_offset"],
        configuration["courtyard_offset"]["connector"],
    ]
    LineDeltaA = [
        0,
        configuration["silk_pad_clearance"] + configuration["silk_line_width"] / 2,
        0,
    ]
    LineWidthA = [
        configuration["fab_line_width"],
        configuration["silk_line_width"],
        configuration["courtyard_line_width"],
    ]
    gridA = [0, 0, configuration["courtyard_grid"]]

    for i, Layer in enumerate(["F.Fab", "F.SilkS", "F.CrtYd"]):
        LineDX = LineDXA[i]
        LineWidth = LineWidthA[i]
        LineDelta = LineDeltaA[i]
        points = []
        grid = gridA[i]

        x1 = 0
        y1 = body_edge["top"] - LineDX

        points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
        #
        x1 = (A / 2) - 1 + LineDX
        y1 = y1
        points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
        #
        x1 = (A / 2) + LineDX
        y1 = y1 + 2
        points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
        #
        x1 = x1
        y1 = mount_pad_y - ((mount_hole_pad_diameter / 2) + LineDX + LineDelta)
        points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
        #
        if Layer == "F.SilkS":  # SilkS
            kicad_mod.append(
                PolygoneLine(polygone=points, layer=Layer, width=LineWidth)
            )
            #
            # Need to do something ugly here, because we will do points = []
            # We need to reflect these points already here
            #
            points2 = []
            for pp in points:
                points2.append([-pp[0], pp[1]])
            kicad_mod.append(
                PolygoneLine(polygone=points2, layer=Layer, width=LineWidth)
            )
            #
            #
            points = []
            x1 = x1
            y1 = mount_pad_y + ((mount_hole_diameter / 2) + LineDX + LineDelta)
            points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
        #
        x1 = x1
        y1 = body_edge["bottom"] + LineDX
        points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
        #
        x1 = (B / 2) + (pad_size[0] / 2) + LineDX + LineDelta
        y1 = y1
        points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
        #
        if Layer == "F.Fab":
            x1 = 0
            y1 = y1
            points.append([roundToBase(x1, grid), roundToBase(y1, grid)])

        if Layer == "F.SilkS":
            ttx1 = x1
            tty1 = y1 + (pad_size[1] / 2)

        if Layer == "F.CrtYd":
            x1 = x1
            y1 = pad_row_1_y + (pad_size[1] / 2) + LineDX
            ttx1 = x1
            tty1 = y1
            points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
            #
            #
            x1 = 0
            y1 = y1
            points.append([roundToBase(x1, grid), roundToBase(y1, grid)])
        #
        # Reflect right part around the X-axis
        #
        points2 = []
        for point in points:
            points2.append([0 - point[0], point[1]])
        #
        #
        if Layer == "F.Fab":  # Fab
            # Add pin 1 marker
            tt = len(points2)
            ps = points2[tt - 1]
            p1 = points2[tt - 2]
            p2 = [(0 - (B / 2)) - 1, p1[1]]
            p3 = [(0 - (B / 2)), p1[1] - 1]
            p4 = [(0 - (B / 2)) + 1, p1[1]]
            points2[tt - 2] = p2
            points2[tt - 1] = p3
            points2.append(p4)
            points2.append(ps)
        elif Layer == "F.SilkS":  # silk
            points2.append([roundToBase(0 - ttx1, grid), roundToBase(tty1, grid)])

        #
        #
        kicad_mod.append(PolygoneLine(polygone=points, layer=Layer, width=LineWidth))
        #
        kicad_mod.append(PolygoneLine(polygone=points2, layer=Layer, width=LineWidth))

    ######################### Text Fields ###############################
    cy_top = roundToBase(
        body_edge["top"] - configuration["courtyard_offset"]["connector"],
        configuration["courtyard_grid"],
    )

    cy_bottom = roundToBase(
        pad_row_1_y + pad_size[1] / 2 + configuration["courtyard_offset"]["connector"],
        configuration["courtyard_grid"],
    )

    addTextFields(
        kicad_mod=kicad_mod,
        configuration=configuration,
        body_edges=body_edge,
        courtyard={"top": cy_top, "bottom": cy_bottom},
        fp_name=footprint_name,
        text_y_inside_position="top",
    )

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get("3d_model_prefix", "${KISYS3DMOD}/")

    lib_name = configuration["lib_name_format_string"].format(
        series=series, man=manufacturer
    )
    model_name = "{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl".format(
        model3d_path_prefix=model3d_path_prefix,
        lib_name=lib_name,
        fp_name=footprint_name,
    )
    kicad_mod.append(Model(filename=model_name))

    output_dir = "{lib_name:s}.pretty/".format(lib_name=lib_name)
    if not os.path.isdir(
        output_dir
    ):  # returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename = "{outdir:s}{fp_name:s}.kicad_mod".format(
        outdir=output_dir, fp_name=footprint_name
    )

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="use confing .yaml files to create footprints."
    )
    parser.add_argument(
        "--global_config",
        type=str,
        nargs="?",
        help="the config file defining how the footprint will look like. (KLC)",
        default="../../tools/global_config_files/config_KLCv3.0.yaml",
    )
    parser.add_argument(
        "--series_config",
        type=str,
        nargs="?",
        help="the config file defining series parameters.",
        default="../conn_config_KLCv3.yaml",
    )
    args = parser.parse_args()

    with open(args.global_config, "r") as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, "r") as config_stream:
        try:
            configuration.update(yaml.safe_load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    for variant in variant_params:
        for pincount in pincount_range:
            generate_one_footprint(pincount, variant, configuration)
