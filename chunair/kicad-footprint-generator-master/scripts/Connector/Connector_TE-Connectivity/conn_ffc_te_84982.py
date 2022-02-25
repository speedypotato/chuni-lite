#!/usr/bin/env python3

'''
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
'''


import argparse
import yaml
import sys
import os

from math import sqrt, ceil, floor

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *
from helpers import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

lib_by_conn_category = True

series = "84982"
manufacturer = 'TE-Connectivity'
conn_category = "FFC-FPC"
orientation = 'V'
datasheet = "https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=84982&DocType=Customer+Drawing&DocLang=English&PartCntxt=84982-8&DocFormat=pdf"

pincounts = range(4, 31)
d_between_rows = 1.8        # [mm]
pad_height_odd = 1.7        # [mm]
pad_height_even = 1.9       # [mm]
pad_width = 0.6             # [mm]
pad_pitch = 1.0             # [mm]
center_to_housing = 1.6     # [mm]
housing_length = 3.0        # [mm]
housing_width_4pin = 6.0    # [mm] 
pins_width_4pin = 3.0       # [mm]
pin1_marker_l = 0.566       # [mm]

def generate_one_footprint(pincount, configuration):
    prefix = "" if (pincount < 10) else "{:d}-".format(floor(pincount / 10))
    partnumber = "{0:s}{1:s}-{2:s}".format(prefix, series, str(pincount)[-1])

    footprint_name = 'TE_{pn:s}_2Rows-{pc:02g}Pins-P1.0mm_Vertical'\
        .format(pn=partnumber, pc=pincount)
    print('Building {:s}'.format(footprint_name))

    # initialise footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription('TE FPC connector, {pc:02g} top-side contacts, 1.0mm pitch, SMT, {ds}'.format(pc=pincount, ds=datasheet))
    kicad_mod.setTags('TE FPC {:s} Vertical Top'.format(partnumber))
    kicad_mod.setAttribute('smd')

    row_offset_odd = (d_between_rows + pad_height_odd) / 2
    row_offset_even = (d_between_rows + pad_height_even) / 2
    housing_y_offset = housing_length / 2

    # create pads
    if bool(pincount % 2):
        upper_pincount = floor(pincount / 2)
        bottom_pincount = ceil(pincount / 2)
    else:
        upper_pincount = bottom_pincount = round(pincount / 2)

    pins_width = pins_width_4pin + (pincount - 4) * pad_pitch
    pin_edge_offset = -pins_width / 2

    kicad_mod.append(PadArray(initial=2, increment=2, pincount=upper_pincount, x_spacing=2 * pad_pitch, start=[pin_edge_offset + pad_pitch, -row_offset_even],
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
        size=[pad_width, pad_height_even], layers=Pad.LAYERS_SMT))

    kicad_mod.append(PadArray(initial=1, increment=2, pincount=bottom_pincount, x_spacing=2 * pad_pitch, start=[pin_edge_offset, row_offset_odd],
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
        size=[pad_width, pad_height_odd], layers=Pad.LAYERS_SMT))

    # create fab outline
    housing_width = housing_width_4pin + (pincount - 4) * pad_pitch
    housing_x_offset = housing_width / 2

    body_edge = {
        'left': -housing_x_offset,
        'right': housing_x_offset,
        'top': -housing_y_offset,
        'bottom': housing_y_offset
    }

    kicad_mod.append(PolygoneLine(
        polygone=[
            [-housing_x_offset, housing_y_offset],
            [housing_x_offset, housing_y_offset],
            [housing_x_offset, -housing_y_offset],
            [-housing_x_offset + pin1_marker_l, -housing_y_offset],
            [-housing_x_offset, -housing_y_offset + pin1_marker_l],
            [-housing_x_offset, housing_y_offset]],
        layer='F.Fab', width=configuration['fab_line_width']))

    # create fab pin 1 marker
    kicad_mod.append(PolygoneLine(
        polygone=[
            [pin_edge_offset - 0.4, housing_y_offset],
            [pin_edge_offset, housing_y_offset - 0.8],
            [pin_edge_offset + 0.4, housing_y_offset]],
        layer='F.Fab', width=configuration['fab_line_width']))

    # create silkscreen outline
    silk_offset = configuration['silk_fab_offset']
    housing_x_offset += silk_offset 
    housing_y_offset += silk_offset

    kicad_mod.append(PolygoneLine(
        polygone=[
            [pin_edge_offset + pad_pitch - pad_width / 2 - 0.2, -housing_y_offset],
            [-housing_x_offset + pin1_marker_l + silk_offset, -housing_y_offset],
            [-housing_x_offset, -housing_y_offset + pin1_marker_l + silk_offset],
            [-housing_x_offset, housing_y_offset],
            [pin_edge_offset - pad_width / 2 - 0.2, housing_y_offset],
            [pin_edge_offset - pad_width / 2 - 0.2, housing_y_offset + pad_height_odd / 2]],
        layer='F.SilkS', width=configuration['silk_line_width']))

    kicad_mod.append(PolygoneLine(
        polygone=[
            [pin_edge_offset + ((bottom_pincount - 1) * 2) * pad_pitch + pad_width / 2 + 0.2, housing_y_offset],
            [housing_x_offset, housing_y_offset],
            [housing_x_offset, -housing_y_offset],
            [pin_edge_offset + ((upper_pincount - 1) * 2 + 1) * pad_pitch + pad_width / 2 + 0.2, -housing_y_offset]],
        layer='F.SilkS', width=configuration['silk_line_width']))

    # create courtyard
    housing_x_offset -= silk_offset 

    courtyard_precision = configuration['courtyard_grid']
    courtyard_clearance = configuration['courtyard_offset']['connector']
    
    courtyard_x = roundToBase(housing_x_offset + courtyard_clearance, courtyard_precision)
    courtyard_y_south = roundToBase(row_offset_odd + pad_height_odd / 2.0 + courtyard_clearance, courtyard_precision)
    courtyard_y_north = roundToBase(row_offset_even + pad_height_even / 2.0 + courtyard_clearance, courtyard_precision)
    
    kicad_mod.append(RectLine(start=[-courtyard_x, courtyard_y_south], end=[courtyard_x, -courtyard_y_north],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))


     ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':-courtyard_y_north, 'bottom':courtyard_y_south}, fp_name=footprint_name, text_y_inside_position=[0, 0])


    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KICAD6_3DMODEL_DIR}/')

    if lib_by_conn_category:
        lib_name = configuration['lib_name_specific_function_format_string'].format(category=conn_category)
    else:
        lib_name = configuration['lib_name_format_string'].format(man=manufacturer)

    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../conn_config_KLCv3.yaml')
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.safe_load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    for pincount in pincounts:
        generate_one_footprint(pincount, configuration)
