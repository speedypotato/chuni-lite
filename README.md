# chuni-lite
kinda cheap slidy air towers for an arcade chuni slider.

Note: I swapped the side the pads are on for chunair_core.  Oops.  Wires will go across the board for now, no biggie.  WS2811/WS2812B optional.

Slider needs:
- HiLetgo 2pcs DB9 Female Adapter RS232 to Terminal RS232 Serial to Terminal DB9 Connector Convert Adapter https://www.amazon.com/gp/product/B082F873KQ (technically just one)
- CQRobot 450 Pieces 2.54mm JST-XA JST Connector Kit. 2.54mm Pitch Female Pin Header, JST XA 2/3 / 4 Pin Housing JST Adapter Cable Connector Socket Male and Female, Crimp DIP Kit. https://www.amazon.com/gp/product/B085QMRHK6 (technically just a 3 & 4 pin)
- USB to VGA/RS-232 Male 9 PIN DB9 Serial Cable 2 FT WIN10/8.1/8/7 PERFECT VISION https://www.amazon.com/gp/product/B097Q5D64Q/ (or any other usb to serial cable)
- 12V 1A PSU minimum with matching female barrel jack that has the screw terminals https://www.amazon.com/gp/product/B091XSVV1Y/

Air towers need:
- 1x USB C Pro Micro
- IR LEDs https://www.amazon.com/gp/product/B01BVGIZGC/ and IR Photodiodes https://www.amazon.com/gp/product/B01BVGIZGM (chanzon ones seem pretty high quality)
- 150 ohm resistor x6
- 10k ohm resistor x6
- some stiff ribbon wire https://www.ebay.com/itm/334199317464 100-Feet Flat Ribbon Cable Grey 50-Conductor 28 AWG Belden 2L28050 008H100
- 12x2mm magnets https://www.ebay.com/itm/391899288494
- Rubber Feet https://www.mcmaster.com/catalog/8884T21
- M3 Nuts
- M4x16 https://www.mcmaster.com/catalog/128/3424
- M3x15 flat head https://www.mcmaster.com/catalog/128/3341
- M3x20 round head https://www.mcmaster.com/catalog/128/3302
- 1 inch hinges https://www.amazon.com/gp/product/B07WJSTNC9 (MroMax 15PCS Door Hinge 1.14" x 0.71" x 0.02" Silver Tone Metal Iron Hinges Brushed Finish Suitable for Door Cabinet Jewelry Case Wooden Box)
- 3D printed parts + a mirrored set
- USB C cable
- Hot Glue

Can hand wire, or replace air_tower_top_1 3D print with chunair pcb.  chunair_core PCB also optional, but is there for ease of wiring(might need to find a way to secure the pro micro as well)

Basic steps:
0. Wire up your slider's 12v and DB9.
1. Print parts.  Then print a mirrored set.
2. Assemble parts with hinge.
3. Glue leds/pds if you are using air_tower_top_1.  Wire according to the diagram in "ac chuni/wiring.png".  If you have PCB, solder resistors and leds/pds
4. Shove unsoldered end of ribbon cable through the channel.
5. Solder to Pro Micro or chunair_core pcb depending on what you have
6. Thread M4 screws through rubber foot and slider to mount to slider.
8. Mount DB9, 12v, and pro micro to mounting plate
7. Unscrew the two m4 screws and add mounting plate with those screws

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
