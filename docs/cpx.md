<div style="text-align:left;color:#990033; font-family:times, serif; font-size:3.0em">The FirmataCPx Firmware</div>
<br>

To monitor and control the Circuit Playground Express, a special version of StandardFirmata, called
**FirmataCPx**, must be installed on the Playground Express.

#Installation

Since the Circuit Playground Express utilizes a UF2 bootloader,
installation is quick and straightforward. To install FirmataCPx onto the
Express, first, click on
[this link](https://github.com/MrYsLab/pymata-cpx/raw/master/FirmataCPxUF2/FirmataCPx.uf2)
to download FirmataCPx.uf2.

Next, place the Circuit Playground Express in bootloader mode by plugging
the Express into a USB port on your computer and double-clicking the
reset button on the Playground Express. All the neo-pixels should light green.

Open up a file explorer tool, and you should see a USB drive called
CPLAYBOOT. Using the file explorer, drag the FirmataCPx.uf2 file onto the CPLAYBOOT entry.
 In a few seconds, FirmataCPx should be
loaded on the Playground Express. The red LED should flash several times and then
extinguish after a successful load. For more information about loading UF2 files onto the Express,
please refer to
[this Adafruit page.](https://learn.adafruit.com/adafruit-circuit-playground-express/downloading-and-flashing)
Even though this page addresses MakeCode, the procedure for flashing a
.uf2 file is the same in all cases.


<br> <br>

Copyright (C) 2019-2021 Alan Yorinks. All Rights Reserved.
