#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","tools")) # load kicad_mod path

from KicadModTree import *  # NOQA
from drawing_tools import *
from footprint_scripts_sip import *

rm=2.54

def recom_78_3pin():
    pins=3
    
    ddrill_large=1.2
    pad_large=[1.7, 2.5]

    ddrill_small=1.0
    pad_small=[1.5, 2.3]    

    package_size=[11.5,8.5,17.5]
    left_offset=3.21
    top_offset=2
    makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill_large, pad=pad_large, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
            footprint_name='Converter_DCDC_RECOM_R-78B-2.0_THT', 
            description="DCDC-Converter, RECOM, RECOM_R-78B-2.0, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78Bxx-2.0.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
            tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
            lib_name='Converter_DCDC')

    package_size=[11.6,8.5,10.4]
    left_offset=package_size[0]-3.21-5.08
    top_offset=package_size[1]-2
    makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill_small, pad=pad_small, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
            footprint_name='Converter_DCDC_RECOM_R-78E-0.5_THT', 
            description="DCDC-Converter, RECOM, RECOM_R-78E-0.5, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78Exx-0.5.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
            tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
            lib_name='Converter_DCDC')

    package_size=[11.5,8.5,17.5]
    left_offset=3.21
    top_offset=2
    pin_bottom_offset=1.5
    makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill_small, pad=pad_small, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
            footprint_name='Converter_DCDC_RECOM_R-78HB-0.5_THT', 
            description="DCDC-Converter, RECOM, RECOM_R-78HB-0.5, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78HBxx-0.5_L.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
            tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
            lib_name='Converter_DCDC')
    makeSIPHorizontal(pins=pins, rm=rm, ddrill=ddrill_small, pad=pad_small, package_size=package_size, left_offset=left_offset, pin_bottom_offset=pin_bottom_offset, 
            footprint_name='Converter_DCDC_RECOM_R-78HB-0.5L_THT', 
            description="DCDC-Converter, RECOM, RECOM_R-78HB-0.5L, SIP-{0}, Horizontally Mounted, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78HBxx-0.5_L.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
            tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
            lib_name='Converter_DCDC')

def recom_78_4pin(): 
    pins=4

    ddrill=1.0
    pad=[1.5, 2.3]

    package_size=[11.6,8.5,10.4]

    left_offset=2
    top_offset=package_size[1]-2
    makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
            footprint_name='Converter_DCDC_RECOM_R-78S-0.1_THT', 
            description="DCDC-Converter, RECOM, RECOM_R-78S-0.1, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-78Sxx-0.1.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
            tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
            lib_name='Converter_DCDC')

def recom_r5():
    pins=12

    ddrill=1.0
    pad=[1.5, 2.3]
    
    package_size=[32.2,9.1,15]
    left_offset=2.1
    top_offset=0.8
    pin_bottom_offset=2
    makeSIPVertical(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, top_offset=top_offset, 
            footprint_name='Converter_DCDC_RECOM_R5xxxPA_THT', 
            description="DCDC-Converter, RECOM, RECOM_R5xxxPA, SIP-{0}, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-5xxxPA_DA.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
            tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
            lib_name='Converter_DCDC')
    makeSIPHorizontal(pins=pins, rm=rm, ddrill=ddrill, pad=pad, package_size=package_size, left_offset=left_offset, pin_bottom_offset=pin_bottom_offset, 
            footprint_name='Converter_DCDC_RECOM_R5xxxDA_THT', 
            description="DCDC-Converter, RECOM, RECOM_R5xxxDA, SIP-{0}, Horizontally Mounted, pitch {1:3.2f}mm, package size {2}x{3}x{4}mm^3, https://www.recom-power.com/pdf/Innoline/R-5xxxPA_DA.pdf".format(pins,rm,package_size[0],package_size[1],package_size[2]), 
            tags="dc-dc recom buck sip-{0} pitch {1:3.2f}mm".format(pins,rm), 
            lib_name='Converter_DCDC')

if __name__ == '__main__':
    recom_78_3pin()
    recom_78_4pin()
    recom_r5()
