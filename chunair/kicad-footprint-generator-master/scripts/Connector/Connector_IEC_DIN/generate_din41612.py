#!/usr/bin/env python3

import sys
import os
import math

sys.path.append(os.path.join(sys.path[0],"..","..","..")) # for KicadModTree
sys.path.append(os.path.join(sys.path[0],"..","..","tools")) # for drawing_tools

from KicadModTree import *
from drawing_tools import *

# According to IEC 60603-2 §3 and DIN 41612-1 §2 connector names should be like
# this:
# "${STANDARD}${TYPE}${PINCOUNT}${GENDER}${METHOD}-${FURTHER_INFO}"
# with:
# STANDARD: either "IEC 60603-2 " or "DIN 41 612-"
# TYPE: B, C, D, E, F, G, H, M, Q, R, S, T, U, V, W
# PINCOUNT: Number of populated pins, 3 digits
# SEX: M: male, F: female
# METHOD: A: screws, C (DIN) crimp (IEC), D: insulation displacement (IEC),
#         K: clamps (DIN), P: press fit (DIN) S: solder, T: blade receptacle,
#         W: wire wrap
# FURTHER_INFO: Pin length, materials and other things that don't change the
#               footprint.
#
# This library choose to use the prefix "Conn_DIN41612_", because Din 41612 is
# more common term.
# METHOD and further are omitted, because the footprint is suited for
# soldering and press fit.
#
# It includes half and third sized connectors, that are not part of IEC 60603
# or DIN 41612. These connectors are named 2X and 3X, a convention also used by
# Harting.



# When a manufacturer is mentioned in the comment, it means that
# the value is explicitly stated in a datasheet by this company.

ROW_IDENTIFIER = ('a', 'b')
LIBRARY_NAME = 'Connector_DIN'
ORIENTATION = {'H': 'Horizontal', 'V': 'Vertical'}

#fp_name_format_string = "Conn_DIN41612_{size:s}{num_pins:d}{gender:s}
#fp_name_format_string = "DIN41612_{size:s}{num_pins:d}{gender:s}_{num_rows:d}x{pins_per_row:d}_{orientation:s}"
fp_name_format_string = "DIN41612_{size:s}_{num_rows:d}x{pins_per_row:d}_{orientation:s}"

def AllPins(row, col):
	return True

def EvenColPins(row, col):
	return not bool(col % 2)

def OptionalPin(kicad_mod, row, col, row_step, col_step, pin_pad, pin_drill, opt_cb, rotate = False):
	if not opt_cb(row, col):
		return
	shape = Pad.SHAPE_CIRCLE
	if col == 1 and row == ROW_IDENTIFIER[0]:
		shape = Pad.SHAPE_RECT
	if rotate:
		x = row_step * (ord(row) - ord(ROW_IDENTIFIER[0]))
		y = -col_step*(col-1)
	else:
		x = col_step*(col-1)
		y = row_step * (ord(row) - ord(ROW_IDENTIFIER[0]))

	kicad_mod.append(Pad(number= row + str(col), type=Pad.TYPE_THT, shape=shape,
			 at=[x, y], size=pin_pad, drill=pin_drill, layers=Pad.LAYERS_THT))
	# don't know if KLC allows 3d compositing at all
	#pin_model = "Pin_Headers.3dshapes/Pin_Header_Straight_1x01_Pitch2.54mm.wrl"
	#inch = 25.4
	#pos_inch = [x/inch, -y/inch, 0]
	#kicad_mod.append(Model(filename=pin_model, at=pos_inch, scale=[1, 1, 1], rotate=[0, 0, 0]))


def BFemale(size, pin_cb, more_description):
	# This footprint is rotated by 90° counter clockwise
	# so columns are in x-direction and rows are in y-direction
	colss = [32, 16, 10]
	cols = colss[size]
	npth_b_offset_x = -0.3 # ERNI and ept
	npth_steps = [90, 50, 34.76] # ERNI and ept
	npth_step = npth_steps[size]
	npth_drill = 2.8 # ERNI and ept
	col_step = -2.54 # ERNI and ept
	row_step = 2.54 # ERNI and ept
	pin_drill = 1 # ERNI and ept
	pin_pad = 1.7 # same as module pinheader
	outer_lengths = [95, 55, 39.76] # maximum value from ERNI and ept
	outer_length = outer_lengths[size]
	outer_width = 8.1 # ERNI and ept
	jack_width = 5.95 # ERNI: 6(-0.1), ept: 5.95(±0.05)
	jack_lengths = [85, 44.4, 29.1] # ERNI
	jack_length = jack_lengths[size]
	notch_depth = 1 # ERNI and ept
	notch_bottom_offset = -3 # ERNI and ept

	mid_x =  0.5 * row_step
	mid_y = -0.5 * col_step * (cols - 1)

	# ------ Init ------
	pin_count = 0;
	for col in range(1, cols + 1):
		pin_count += int(pin_cb('A', col))
		pin_count += int(pin_cb('B', col))
	#size_names = ["B", "2B", "3B"]
	size_names = ["B", "B2", "B3"]
	footprint_name = fp_name_format_string.format(
		size=size_names[size], num_pins=pin_count, gender="F",
		num_rows=2, pins_per_row=pin_count//2, orientation=ORIENTATION['V'])

	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	size_descs = ["B", "B/2", "B/3"]
	kicad_mod.setDescription("DIN 41612 connector, type " + size_descs[size] + ", vertical, " + str(cols) + " pins wide, 2 rows" + more_description)
	kicad_mod.setTags("DIN 41512 IEC 60603 " + size_descs[size])

	# ------ Pins and holes ------
	for col in range(1, cols + 1):
		OptionalPin(kicad_mod, ROW_IDENTIFIER[0], col, row_step, col_step, pin_pad, pin_drill, pin_cb, True)
		OptionalPin(kicad_mod, ROW_IDENTIFIER[1], col, row_step, col_step, pin_pad, pin_drill, pin_cb, True)

	# non-plated drill holes, assumed to be equally distant to pins
	npth_x = row_step + npth_b_offset_x
	npth_y_left  = mid_y - npth_step * 0.5
	npth_y_right = mid_y + npth_step * 0.5
	kicad_mod.append(Pad(number="", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
					 at=[npth_x, npth_y_left], size=npth_drill, drill=npth_drill, layers=Pad.LAYERS_NPTH))
	kicad_mod.append(Pad(number="", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
					 at=[npth_x, npth_y_right], size=npth_drill, drill=npth_drill, layers=Pad.LAYERS_NPTH))


	# ------ Courtyard ------
	# KLC: connectors should have 0.5mm clearance
	kicad_mod.append(RectLine(
		start=[mid_x - outer_width/2 - 0.5, mid_y - outer_length/2 - 0.5],
		end=[mid_x + outer_width/2 + 0.5, mid_y + outer_length/2 + 0.5],
		layer='F.CrtYd'))

	# ------ Fabrication layer ------
	j_t_x = mid_x - jack_width * 0.5 # jack top
	j_b_x = mid_x + jack_width * 0.5 # jack bottom
	j_l_y = mid_y - jack_length * 0.5 # jack left
	j_r_y = mid_y + jack_length * 0.5 # jack right
	n_x  = j_b_x + notch_bottom_offset # notch
	n_l_y = j_l_y + notch_depth # notch left
	n_r_y = j_r_y - notch_depth # notch right

	jack_notch_left  = [[j_t_x, n_l_y], [j_t_x, j_l_y], [n_x, j_l_y], [n_x, n_l_y], [j_b_x, n_l_y]]
	jack_notch_right = [[j_b_x, n_r_y], [n_x, n_r_y], [n_x, j_r_y], [j_t_x, j_r_y], [j_t_x, n_r_y]]
	pin_a1_arrow = [ # form taken from module Connectors_Molex
		[mid_x - outer_width/2 - 0.2,  0.0],
		[mid_x - outer_width/2 - 0.8, -0.3],
		[mid_x - outer_width/2 - 0.8,  0.3],
		[mid_x - outer_width/2 - 0.2,  0.0],
	]

	kicad_mod.append(PolygoneLine(
		polygone=jack_notch_left + jack_notch_right + [jack_notch_left[0]],
		layer='F.Fab'))
	kicad_mod.append(PolygoneLine(
		polygone=pin_a1_arrow,
		width=0.12,
		layer='F.Fab'))
	kicad_mod.append(Text(
		type='value', text=footprint_name,
		at=[mid_x, mid_y + outer_length/2 + 1.3],
		layer='F.Fab'))
	# Very small Reference Designator to fit between the pins.
	kicad_mod.append(Text(
		type='user', text='%R',
		at=[mid_x, mid_y],
		size=[0.6, 0.6], thickness=0.07,
		layer='F.Fab'))

	# ------ Silk screen ------
	# assume plastic part to be centered around the pins
	# silk screen must be visible, so add 0.1 mm
	kicad_mod.append(RectLine(
		start=[mid_x - outer_width/2 - 0.1, mid_y - outer_length/2 - 0.1],
		end=[mid_x + outer_width/2 + 0.1, mid_y + outer_length/2 + 0.1],
		width=0.15,
		layer='F.SilkS'))
	kicad_mod.append(PolygoneLine(
		polygone=jack_notch_left,
		width=0.15,
		layer='F.SilkS'))
	kicad_mod.append(PolygoneLine(
		polygone=jack_notch_right,
		width=0.15,
		layer='F.SilkS'))
	kicad_mod.append(PolygoneLine(
		polygone=pin_a1_arrow,
		width=0.12,
		layer='F.SilkS'))
	kicad_mod.append(Text(
		type='reference', text='REF**',
		at=[mid_x, mid_y - outer_length/2 - 1],
		layer='F.SilkS'))

	# ------ 3D reference ------
	# in case someone wants to make a model
	kicad_mod.append(Model(
		filename="${KICAD6_3DMODEL_DIR}/Connectors_IEC_DIN.3dshapes/" + footprint_name + ".wrl",
		at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

	# ------ Output ------
	file_handler = KicadFileHandler(kicad_mod)

	output_dir = '{lib_name:s}.pretty/'.format(lib_name=LIBRARY_NAME)
	if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
		os.makedirs(output_dir)
	filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

	file_handler.writeFile(filename)


def BMale(size, pin_cb, more_description):
	colss = [32, 16, 10]
	cols = colss[size]
	npth_a_offset_y = -2.54 # ERNI
	npth_steps = [88.9, 48.26, 33.02] # ERNI
	npth_step = npth_steps[size]
	npth_drill = 2.8 # ERNI
	col_step = 2.54 # ERNI and ept
	row_step = 2.54 # ERNI and ept
	pin_drill = 1 # ERNI and ept
	pin_pad = 1.7 # same as module pinheader
	jack_to_npth = 10.2 # ERNI
	jack_widths = [87.5, 47, 31.7] # ERNI
	jack_width = jack_widths[size]
	jack_to_eyelet = 12.7
	eyelet_spans = [94, 53.5, 38.1] # ERNI or ept
	eyelet_span = eyelet_spans[size]
	board_edge_to_a = 5.3 # ERNI

	mid_x = 0.5 * col_step * (cols - 1)
	mid_y = 0.5 * row_step

	# ------ Init ------
	pin_count = 0;
	for col in range(1, cols + 1):
		pin_count += int(pin_cb('A', col))
		pin_count += int(pin_cb('B', col))
	#size_names = ["B", "2B", "3B"]
	size_names = ["B", "B2", "B3"]
	footprint_name = fp_name_format_string.format(
		size=size_names[size], num_pins=pin_count, gender="M",
		num_rows=2, pins_per_row=pin_count//2, orientation=ORIENTATION['H'])

	# init kicad footprint
	kicad_mod = Footprint(footprint_name)
	size_descs = ["B", "B/2", "B/3"]
	kicad_mod.setDescription("DIN 41612 connector, type " + size_descs[size] + ", horizontal, " + str(cols) + " pins wide, 2 rows" + more_description)
	kicad_mod.setTags("DIN 41512 IEC 60603 " + size_descs[size])

	# ------ Pins and holes ------
	for col in range(1, cols + 1):
		OptionalPin(kicad_mod, ROW_IDENTIFIER[0], col, row_step, col_step, pin_pad, pin_drill, pin_cb)
		OptionalPin(kicad_mod, ROW_IDENTIFIER[1], col, row_step, col_step, pin_pad, pin_drill, pin_cb)

	# non-plated drill holes, assumed to be equally distant to pins
	npth_x_left  = mid_x - npth_step * 0.5
	npth_x_right = mid_x + npth_step * 0.5
	npth_y = npth_a_offset_y
	kicad_mod.append(Pad(number="", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
					 at=[npth_x_left, npth_y], size=npth_drill, drill=npth_drill, layers=Pad.LAYERS_NPTH))
	kicad_mod.append(Pad(number="", type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
					 at=[npth_x_right, npth_y], size=npth_drill, drill=npth_drill, layers=Pad.LAYERS_NPTH))

	# ------ Silk screen ------
	# assume plastic part to be centered around the pins
	eyelet_border = jack_to_eyelet - jack_to_npth
	package_outline = [
		[mid_x - eyelet_span/2 + 2 * eyelet_border, npth_y + eyelet_border - pin_drill/2], # x: guess
		[mid_x - eyelet_span/2 + 2 * eyelet_border, npth_y + eyelet_border], # x: guess
		[mid_x - eyelet_span/2, npth_y + eyelet_border],
		[mid_x - eyelet_span/2, npth_y - eyelet_border], # y: guess, not ept
		[mid_x - jack_width/2, npth_y - eyelet_border], # y: guess, not ept
		[mid_x - jack_width/2, npth_y - jack_to_npth],
		# --- mirror line ---
		[mid_x + jack_width/2, npth_y - jack_to_npth],
		[mid_x + jack_width/2, npth_y - eyelet_border], # y: guess, not ept
		[mid_x + eyelet_span/2, npth_y - eyelet_border], # y: guess, not ept
		[mid_x + eyelet_span/2, npth_y + eyelet_border],
		[mid_x + eyelet_span/2 - 2 * eyelet_border, npth_y + eyelet_border], # x: guess
		[mid_x + eyelet_span/2 - 2 * eyelet_border, npth_y + eyelet_border - pin_drill/2], # x: guess
	]
	# silkscreen is offset by 0.1 mm to be visible with component placed
	silkscreen_left = [
		[package_outline[ 0][0] + 0.1, package_outline[ 0][1] + 0.1],
		[package_outline[ 1][0] + 0.1, package_outline[ 1][1] + 0.1],
		[package_outline[ 2][0] - 0.1, package_outline[ 2][1] + 0.1],
		[package_outline[ 3][0] - 0.1, package_outline[ 3][1]],
		# can not draw further, it would leave the pcb
	]
	silkscreen_right = [
		[package_outline[11][0] - 0.1, package_outline[11][1] + 0.1],
		[package_outline[10][0] - 0.1, package_outline[10][1] + 0.1],
		[package_outline[ 9][0] + 0.1, package_outline[ 9][1] + 0.1],
		[package_outline[ 8][0] + 0.1, package_outline[ 8][1]],
		# can not draw further, it would leave the pcb
	]
	pin_a1_arrow = [ # form taken from module Connectors_Molex
		[-pin_pad/2 - 0.5 - 0.0, 0.0],
		[-pin_pad/2 - 0.5 - 0.6, -0.3],
		[-pin_pad/2 - 0.5 - 0.6, 0.3],
		[-pin_pad/2 - 0.5 - 0.0, 0.0]
	]
	kicad_mod.append(PolygoneLine(
		polygone=silkscreen_left,
		width=0.15,
		layer='F.SilkS'))
	kicad_mod.append(PolygoneLine(
		polygone=silkscreen_right,
		width=0.15,
		layer='F.SilkS'))
	kicad_mod.append(PolygoneLine(
		polygone=pin_a1_arrow,
		width=0.12,
		layer='F.SilkS'))
	kicad_mod.append(Text(
		type='reference', text='REF**',
		at=[mid_x - npth_step * 0.5, row_step * 0.5],
		layer='F.SilkS'))

	# ------ Fabrication layer ------
	kicad_mod.append(PolygoneLine(
		polygone = package_outline + [package_outline[0]],
		layer = 'F.Fab'))
	kicad_mod.append(Text(
		type='value', text=footprint_name,
		at=[mid_x, npth_y + jack_to_npth - 1.3],
		layer='F.Fab'))
	kicad_mod.append(Text(
		type='user', text='%R',
		at=[mid_x, npth_y],
		size=[1, 1], thickness=0.15,
		layer='F.Fab'))

	# ------ Courtyard ------
	# KLC: connectors should have 0.5mm clearance
	courtyard = [
		[-pin_pad/2 - 0.5, row_step + pin_pad/2 + 0.5],
		[-pin_pad/2 - 0.5, package_outline[10][1] + 0.5],
		[package_outline[ 2][0] - 0.5, package_outline[ 2][1] + 0.5],
		[package_outline[ 3][0] - 0.5, package_outline[ 3][1] - 0.5],
		[package_outline[ 4][0] - 0.5, package_outline[ 4][1] - 0.5],
		[package_outline[ 5][0] - 0.5, package_outline[ 5][1] - 0.5],
		[package_outline[ 6][0] + 0.5, package_outline[ 6][1] - 0.5],
		[package_outline[ 7][0] + 0.5, package_outline[ 7][1] - 0.5],
		[package_outline[ 8][0] + 0.5, package_outline[ 8][1] - 0.5],
		[package_outline[ 9][0] + 0.5, package_outline[ 9][1] + 0.5],
		[package_outline[10][0] - 0.5, package_outline[10][1] + 0.5],
		[(cols - 1) * col_step + pin_pad/2 + 0.5, package_outline[ 1][1] + 0.5],
		[(cols - 1) * col_step + pin_pad/2 + 0.5, row_step + pin_pad/2 + 0.5],
	]
	kicad_mod.append(PolygoneLine(
		polygone = courtyard + [courtyard[0]],
		layer = 'F.CrtYd'))

	# ------ Board edge ------
	kicad_mod.append(Line(
		start = [mid_x - jack_width/2, -board_edge_to_a],
		end = [mid_x + jack_width/2, -board_edge_to_a],
		width = 0.08,
		layer = 'Dwgs.User'))
	kicad_mod.append(Line(
		start = [mid_x, -board_edge_to_a - 1.5],
		end = [mid_x, -board_edge_to_a - 0.1],
		width = 0.1,
		layer = 'Cmts.User'))
	kicad_mod.append(PolygoneLine(
		polygone = [
			[mid_x - 0.2, -board_edge_to_a - 0.6],
			[mid_x, -board_edge_to_a - 0.1],
			[mid_x + 0.2, -board_edge_to_a - 0.6],
		],
		width = 0.1,
		layer = 'Cmts.User'))
	kicad_mod.append(Text(
		type='user', text='Board edge',
		at=[mid_x, -board_edge_to_a - 2],
		size=[0.7, 0.7], thickness=0.1,
		layer='Cmts.User'))

	# ------ 3D reference ------
	# in case someone wants to make a model
	kicad_mod.append(Model(
		filename="{prefix}{lib_name}.3dshapes/{fp_name}.wrl".format(prefix = '${KICAD6_3DMODEL_DIR}/', lib_name=LIBRARY_NAME, fp_name=footprint_name),
		at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

	# ------ Output ------
	file_handler = KicadFileHandler(kicad_mod)

	output_dir = '{lib_name:s}.pretty/'.format(lib_name=LIBRARY_NAME)
	if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
		os.makedirs(output_dir)
	filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

	file_handler.writeFile(filename)




BFemale(0, AllPins, ", full configuration")
BFemale(0, EvenColPins, ", even columns")
BFemale(1, AllPins, ", full configuration")
BFemale(1, EvenColPins, ", even columns")
BFemale(2, AllPins, ", full configuration")
BFemale(2, EvenColPins, ", even columns")

BMale(0, AllPins, ", full configuration")
BMale(0, EvenColPins, ", even columns")
BMale(1, AllPins, ", full configuration")
BMale(1, EvenColPins, ", even columns")
BMale(2, AllPins, ", full configuration")
BMale(2, EvenColPins, ", even columns")

# output kicad model
