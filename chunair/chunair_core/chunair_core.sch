EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Conn_01x08_Male J1
U 1 1 6219D996
P 5250 3050
F 0 "J1" V 5177 2978 50  0000 C CNN
F 1 "Conn_01x08_Male" V 5086 2978 50  0000 C CNN
F 2 "chunair_local:SMD_8Pin" H 5250 3050 50  0001 C CNN
F 3 "~" H 5250 3050 50  0001 C CNN
	1    5250 3050
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x08_Male J2
U 1 1 6219F82A
P 5250 4000
F 0 "J2" V 5177 3928 50  0000 C CNN
F 1 "Conn_01x08_Male" V 5086 3928 50  0000 C CNN
F 2 "chunair_local:SMD_8Pin" H 5250 4000 50  0001 C CNN
F 3 "~" H 5250 4000 50  0001 C CNN
	1    5250 4000
	0    -1   -1   0   
$EndComp
$Comp
L power:+5V #PWR01
U 1 1 621A1491
P 4950 2850
F 0 "#PWR01" H 4950 2700 50  0001 C CNN
F 1 "+5V" H 4965 3023 50  0000 C CNN
F 2 "" H 4950 2850 50  0001 C CNN
F 3 "" H 4950 2850 50  0001 C CNN
	1    4950 2850
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR07
U 1 1 621A1B83
P 4950 3800
F 0 "#PWR07" H 4950 3650 50  0001 C CNN
F 1 "+5V" H 4965 3973 50  0000 C CNN
F 2 "" H 4950 3800 50  0001 C CNN
F 3 "" H 4950 3800 50  0001 C CNN
	1    4950 3800
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR02
U 1 1 621A2541
P 5350 2850
F 0 "#PWR02" H 5350 2600 50  0001 C CNN
F 1 "GND" H 5355 2677 50  0000 C CNN
F 2 "" H 5350 2850 50  0001 C CNN
F 3 "" H 5350 2850 50  0001 C CNN
	1    5350 2850
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR08
U 1 1 621A2FDE
P 5350 3800
F 0 "#PWR08" H 5350 3550 50  0001 C CNN
F 1 "GND" H 5355 3627 50  0000 C CNN
F 2 "" H 5350 3800 50  0001 C CNN
F 3 "" H 5350 3800 50  0001 C CNN
	1    5350 3800
	-1   0    0    1   
$EndComp
Text Label 5050 2850 0    50   ~ 0
6
Text Label 5050 3800 0    50   ~ 0
7
Text Label 5150 2850 0    50   ~ 0
8
Text Label 5150 3800 0    50   ~ 0
16
Text Label 5250 2850 0    50   ~ 0
14
Text Label 5250 3800 0    50   ~ 0
15
Text Label 5450 2850 0    50   ~ 0
A10
Text Label 5450 3800 0    50   ~ 0
A9
Text Label 5550 3800 0    50   ~ 0
A0
Text Label 5550 2850 0    50   ~ 0
A1
Text Label 5650 3800 0    50   ~ 0
A2
Text Label 5650 2850 0    50   ~ 0
A3
$Comp
L promicro:ProMicro U1
U 1 1 621A4D99
P 3200 4050
F 0 "U1" H 3200 5087 60  0000 C CNN
F 1 "ProMicro" H 3200 4981 60  0000 C CNN
F 2 "promicro:ProMicro-EnforcedTop" H 3300 3000 60  0001 C CNN
F 3 "" H 3300 3000 60  0000 C CNN
	1    3200 4050
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR06
U 1 1 621A651C
P 3900 3600
F 0 "#PWR06" H 3900 3450 50  0001 C CNN
F 1 "+5V" V 3915 3728 50  0000 L CNN
F 2 "" H 3900 3600 50  0001 C CNN
F 3 "" H 3900 3600 50  0001 C CNN
	1    3900 3600
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR04
U 1 1 621A722C
P 2500 3500
F 0 "#PWR04" H 2500 3250 50  0001 C CNN
F 1 "GND" V 2505 3372 50  0000 R CNN
F 2 "" H 2500 3500 50  0001 C CNN
F 3 "" H 2500 3500 50  0001 C CNN
	1    2500 3500
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR05
U 1 1 621A83D0
P 2500 3600
F 0 "#PWR05" H 2500 3350 50  0001 C CNN
F 1 "GND" V 2505 3472 50  0000 R CNN
F 2 "" H 2500 3600 50  0001 C CNN
F 3 "" H 2500 3600 50  0001 C CNN
	1    2500 3600
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR03
U 1 1 621A869C
P 3900 3400
F 0 "#PWR03" H 3900 3150 50  0001 C CNN
F 1 "GND" V 3905 3272 50  0000 R CNN
F 2 "" H 3900 3400 50  0001 C CNN
F 3 "" H 3900 3400 50  0001 C CNN
	1    3900 3400
	0    -1   -1   0   
$EndComp
Text Label 2500 4100 2    50   ~ 0
6
Text Label 2500 4200 2    50   ~ 0
7
Text Label 2500 4300 2    50   ~ 0
8
Text Label 2500 4400 2    50   ~ 0
A9
Text Label 3900 4400 0    50   ~ 0
A10
Text Label 3900 4300 0    50   ~ 0
16
Text Label 3900 4200 0    50   ~ 0
14
Text Label 3900 4100 0    50   ~ 0
15
Text Label 3900 4000 0    50   ~ 0
A0
Text Label 3900 3900 0    50   ~ 0
A1
Text Label 3900 3800 0    50   ~ 0
A2
Text Label 3900 3700 0    50   ~ 0
A3
$Comp
L Mechanical:MountingHole H1
U 1 1 621C1733
P 10450 750
F 0 "H1" H 10550 796 50  0000 L CNN
F 1 "MountingHole" H 10550 705 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 10450 750 50  0001 C CNN
F 3 "~" H 10450 750 50  0001 C CNN
	1    10450 750 
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 621C1D64
P 10450 1150
F 0 "H2" H 10550 1196 50  0000 L CNN
F 1 "MountingHole" H 10550 1105 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 10450 1150 50  0001 C CNN
F 3 "~" H 10450 1150 50  0001 C CNN
	1    10450 1150
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x03_Male J3
U 1 1 621C27A2
P 5300 5150
F 0 "J3" V 5454 4962 50  0000 R CNN
F 1 "Conn_01x03_Male" V 5363 4962 50  0000 R CNN
F 2 "chunair_local:SMD_3Pin" H 5300 5150 50  0001 C CNN
F 3 "~" H 5300 5150 50  0001 C CNN
	1    5300 5150
	0    -1   -1   0   
$EndComp
Text Label 5200 4950 1    50   ~ 0
RGB_L
Text Label 5300 4950 1    50   ~ 0
RGB_R
Text Label 5400 4950 1    50   ~ 0
coin
Text Label 2500 4000 2    50   ~ 0
coin
Text Label 2500 3900 2    50   ~ 0
RGB_R
Text Label 2500 3800 2    50   ~ 0
RGB_L
$Comp
L Mechanical:MountingHole H3
U 1 1 621CE0F8
P 10450 1550
F 0 "H3" H 10550 1596 50  0000 L CNN
F 1 "MountingHole" H 10550 1505 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 10450 1550 50  0001 C CNN
F 3 "~" H 10450 1550 50  0001 C CNN
	1    10450 1550
	1    0    0    -1  
$EndComp
$EndSCHEMATC
