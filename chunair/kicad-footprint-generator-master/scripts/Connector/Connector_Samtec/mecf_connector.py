#!/usr/bin/env python3

import sys
import os
import math

from operator import add
from helpers import *
from math import sqrt
import argparse
import yaml

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0], "..", "..", "..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0], "..", "..", "tools")) # load kicad_mod path

from KicadModTree import *  # NOQA
# from drawing_tools import *
# from footprint_scripts_potentiometers import *
from footprint_text_fields import addTextFields

lib_name_category = 'PCBEdge'

pinrange = ['05', '08', '20', '30', '40', '50', '60', '70']

pad_size = [0.56,4.00]
layers_top = ['F.Cu', 'F.Mask']
layers_bottom = ['B.Cu', 'B.Mask']

pad_type = Pad.TYPE_CONNECT


K = {   '05': 8.10,
        '08': 11.91,
        '20': 27.15,
        '30': 39.85,
        '40': 52.55,
        '50': 65.25,
        '60': 77.95,
        '70': 90.65
    }

L = {   '05': 2.79,
        '08': 4.06,
        '20': 10.41,
        '30': 14.22,
        '40': 20.57,
        '50': 26.92,
        '60': 20.57,
        '70': 34.54
    }

M = {   '60': 40.89,
        '70': 73.91
    }

POL = { '05': [ 3],
        '08': [ 5],
        '20': [15],
        '30': [21],
        '40': [31],
        '50': [41],
        '60': [31, 63],
        '70': [53, 115]
      }

def generate_one_footprint(pol, n, configuration):
    off = configuration['silk_fab_offset']
    CrtYd_offset = configuration['courtyard_offset']['default']
    fp_name = 'Samtec_MECF-' + n + '-0_-'
    if pol == False:
        fp_name = fp_name + 'NP-'
    fp_name += 'L-DV'

    fp_name += '_{:d}x{:02d}_P{:.2f}mm'.format(2,int(n),1.27)
    if pol:
        fp_name += '_Polarized'
    fp_name += '_Edge'

    kicad_mod = Footprint(fp_name)

    description = "Highspeed card edge connector for PCB's with " + n + " contacts "

    if pol == True:
        description = description + '(polarized)'
    else:
        description = description + '(not polarized)'

    kicad_mod.setAttribute('virtual')

    #set the FP description
    kicad_mod.setDescription(description)

    tags = "conn samtec card-edge high-speed"

    #set the FP tags
    kicad_mod.setTags(tags)


    # set general values

    top = -(5.0)
    bot =  (5.0)

    left = -(K[n]/2.0)
    right = (K[n]/2.0)
    body_edge={
        'left': left,
        'right': right,
        'top': top,
        'bottom': bot
    }

    top_left =  [left, top]
    bot_right = [ right, bot]

    # create Fab Back(exact outline)
    kicad_mod.append(Line(start=[left + 1.27, bot], end=[right, bot],
        layer='F.Fab', width=configuration['fab_line_width']))   #bot line
    kicad_mod.append(Line(start=[left, top], end=[ right, top],
        layer='F.Fab', width=configuration['fab_line_width']))   #top line
    kicad_mod.append(Line(start=[left, bot - 1.27], end=[left, top],
        layer='F.Fab', width=configuration['fab_line_width']))   #left line
    kicad_mod.append(Line(start=[right, bot], end=[ right, top],
        layer='F.Fab', width=configuration['fab_line_width']))   #right line
    kicad_mod.append(Line(start=[left, bot - 1.27], end=[left + 1.27, bot],
        layer='F.Fab', width=configuration['fab_line_width']))   #corner

    # create Fab Front(exact outline)
    kicad_mod.append(Line(start=[left, bot], end=[right, bot],
        layer='B.Fab', width=configuration['fab_line_width']))   #bot line
    kicad_mod.append(Line(start=[left, top], end=[ right, top],
        layer='B.Fab', width=configuration['fab_line_width']))   #top line
    kicad_mod.append(Line(start=[left, bot ], end=[left, top],
        layer='B.Fab', width=configuration['fab_line_width']))   #left line
    kicad_mod.append(Line(start=[right, bot], end=[ right, top],
        layer='B.Fab', width=configuration['fab_line_width']))   #right line


    top = top - off
    #bot = bot + 0.11
    left = left - off
    right = right + off

    # create silscreen Back(exact + 0.11)
    kicad_mod.append(Line(start=[round(left, 2) + 1.27, round(bot, 2)],
                          end=[round(right, 2), round(bot, 2)],
                          layer='F.SilkS', width=configuration['silk_line_width'])) #bot line
    kicad_mod.append(Line(start=[round(left, 2), round(top, 2)],
                          end=[round(right, 2), round(top, 2)],
                          layer='F.SilkS', width=configuration['silk_line_width'])) #top line
    kicad_mod.append(Line(start=[round(left, 2), round(bot, 2) - 1.27],
                          end=[round(left, 2), round(top, 2)],
                          layer='F.SilkS', width=configuration['silk_line_width'])) #left line
    kicad_mod.append(Line(start=[round(right, 2), round( bot, 2)],
                          end=[round(right, 2), round(top, 2)],
                          layer='F.SilkS', width=configuration['silk_line_width'])) #right line
    kicad_mod.append(Line(start=[round(left, 2) + 1.27, round(bot, 2) ],
                          end=[round(left, 2), round(bot, 2) - 1.27],
                          layer='F.SilkS', width=configuration['silk_line_width']))   #corner

    # create silscreen Front(exact + 0.11)
    kicad_mod.append(Line(start=[round(left, 2), round(bot, 2)],
                          end=[round(right, 2), round(bot, 2)],
                          layer='B.SilkS', width=configuration['silk_line_width'])) #bot line
    kicad_mod.append(Line(start=[round(left, 2), round(top, 2)],
                          end=[round(right, 2), round(top, 2)],
                          layer='B.SilkS', width=configuration['silk_line_width'])) #top line
    kicad_mod.append(Line(start=[round(left, 2), round(bot, 2)],
                          end=[round(left, 2), round(top, 2)],
                          layer='B.SilkS', width=configuration['silk_line_width'])) #left line
    kicad_mod.append(Line(start=[round(right, 2), round( bot, 2)],
                          end=[round(right, 2), round(top, 2)],
                          layer='B.SilkS', width=configuration['silk_line_width'])) #right line

    top = roundToBase(body_edge['top'] - CrtYd_offset, configuration['courtyard_grid'])
    bot = roundToBase(body_edge['bottom'], configuration['courtyard_grid'])
    left = roundToBase(body_edge['left'] - CrtYd_offset, configuration['courtyard_grid'])
    right = roundToBase(body_edge['right'] + CrtYd_offset, configuration['courtyard_grid'])

    cy1 = top
    cy2 = bot

    # create courtyard (exact + 0.25)
    kicad_mod.append(RectLine(start=[left, top], end=[right , bot],
            layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(RectLine(start=[left, top], end=[right , bot],
            layer='B.CrtYd', width=configuration['courtyard_line_width']))




    top = body_edge['top']
    bot =  body_edge['bottom']
    slot_height = 7.0


    ## create cutout
    kicad_mod.append(Line(start=[-K[n]/2.0, bot, 2],
                          end=[-K[n]/2.0, top, 2], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #left line
    kicad_mod.append(Line(start=[K[n]/2.0, bot, 2],
                          end=[K[n]/2.0, top], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #right line


    ## grid ends
    nextGrid = math.ceil((K[n]/2.0)/0.25 + 1.0) * 0.25
    #nextGrid = roundToBase(K[n]/2, 0.25)
    kicad_mod.append(Line(start=[-nextGrid, top, 2],
        end=[-K[n]/2.0, top, 2], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #left line
    kicad_mod.append(Line(start=[+nextGrid, top, 2],
        end=[K[n]/2.0, top], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #right line



    if pol == True:   # Cutouts

        kicad_mod.append(Line(start=[-K[n]/2.0, bot],
                              end=[-K[n]/2.0+L[n]-1.24/2.0, bot], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #bot line

        kicad_mod.append(Line(start=[-K[n]/2.0+L[n]-1.24/2.0, bot],
                              end=[-K[n]/2.0+L[n]-1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #up
        kicad_mod.append(Line(start=[-K[n]/2.0+L[n]+1.24/2.0, bot],
                              end=[-K[n]/2.0+L[n]+1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #down
        kicad_mod.append(Line(start=[-K[n]/2.0+L[n]-1.24/2.0, bot - slot_height],
                              end=[-K[n]/2.0+L[n]+1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #cut

        if n in ['60','70']:
            kicad_mod.append(Line(start=[-K[n]/2.0+L[n]+1.24/2.0, bot],
                              end=[-K[n]/2.0+M[n]-1.24/2.0, bot], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #bot line

            kicad_mod.append(Line(start=[-K[n]/2.0+M[n]-1.24/2.0, bot],
                              end=[-K[n]/2.0+M[n]-1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #up
            kicad_mod.append(Line(start=[-K[n]/2.0+M[n]+1.24/2.0, bot],
                              end=[-K[n]/2.0+M[n]+1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #down
            kicad_mod.append(Line(start=[-K[n]/2.0+M[n]-1.24/2.0, bot - slot_height],
                              end=[-K[n]/2.0+M[n]+1.24/2.0, bot - slot_height], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #cut

            kicad_mod.append(Line(start=[-K[n]/2.0+M[n]+1.24/2.0, bot],
                              end=[K[n]/2.0, bot], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #bot line
        else:
            kicad_mod.append(Line(start=[-K[n]/2.0+L[n]+1.24/2.0, bot],
                              end=[K[n]/2.0, bot], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #bot line

    else:
        kicad_mod.append(Line(start=[-K[n]/2.0, bot],
                              end=[K[n]/2.0, bot], layer='Edge.Cuts', width=configuration['edge_cuts_line_width'])) #bot line



    # create pads
    for i in range(0,int(n)):
        start = - K[n]/2.0 + 1.52

        if pol == True:
            if (i*2+1) not in POL[n]:
                kicad_mod.append(Pad(number=i*2 + 1, type=pad_type, shape=Pad.SHAPE_RECT,
                    at=[start + i*1.27, bot - 2.0 - 0.5], size=pad_size, layers=layers_top))
                kicad_mod.append(Pad(number=i*2 + 2, type=pad_type, shape=Pad.SHAPE_RECT,
                    at=[start + i*1.27, bot - 2.0 - 0.5], size=pad_size, layers=layers_bottom))
        else:
            kicad_mod.append(Pad(number=i*2 + 1, type=pad_type, shape=Pad.SHAPE_RECT,
                at=[start + i*1.27, bot - 2.0 - 0.5], size=pad_size, layers=layers_top))
            kicad_mod.append(Pad(number=i*2 + 2, type=pad_type, shape=Pad.SHAPE_RECT,
                at=[start + i*1.27, bot - 2.0 - 0.5], size=pad_size, layers=layers_bottom))



    # output kicad model
    #print(kicad_mod

    # print render tree
    #print(kicad_mod.getRenderTree())
    #print(kicad_mod.getCompleteRenderTree())

    # kicad_mod.append(Text(type='reference', text='REF**', at=[0,-6.35], layer='F.SilkS'))
    # kicad_mod.append(Text(type='user', text='%R', at=[0,-2.54], layer='F.Fab'))
    # kicad_mod.append(Text(type='value', text=fp_name, at=[0,-3.81], layer='F.Fab'))
    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=fp_name, text_y_inside_position=-2.54)

    lib_name = configuration['lib_name_specific_function_format_string'].format(category=lib_name_category)
    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=fp_name)


    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)



if __name__ == "__main__":
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

    for pol in [True, False]:
        for pincount in pinrange:
            generate_one_footprint(pol, pincount, configuration)
