## An Overview Of Using The OneGPIO Extensions

Now that all the necessary software is installed on your computer
and your physical computing device, it is time to try things out.

Here is a brief recommended procedure for using Scratch 3 with your
physical computing projects:

**Step 1:** With the power disconnected from your micro-controller, attach
the sensors and actuators to the micro-controller. **Never** add or
remove sensors or actuators with power applied - you may permanently
damage your micro-controller.
   
**Step 2:** Apply power to the micro-controller.

**Step 3:** Start the OneGPIO server code by opening a terminal 
window for each microcontroller you wish to use. Then, enter the command for the specific micro-controller:
   
   * **s3a** - for the Arduino
   * **s3c** - for the Adafruit Circuit Playground Express
*    **s3e** - for the ESP-8266
*  **s3p** - for the Picoboard
   * **s3r** - for the Raspberry Pi
   * **s3rh** - for the RoboHAT MM1
   
**Step 4:** Start Scratch 3, select an extension, and create and run
your Scratch scripts. If you are using the ESP-8266 extension, you must use the **ESP-8266 Connect IP Address** block, 
to connect to the ESP-8266. When successfully connected, 
the red LED on the ESP-8266
NodeMCU is extinguished.

**Step 5:** To power down, dismiss the OneGPIO server by going to the
window opened in step 3 and pressing Control-C. You may need to do this
twice. Finally, dismiss the Web Browser tab running
Scratch 3. **SPECIAL NOTE:** Please use Control-C before dismissing the window.
If you dismiss the window without pressing Control-C first, the next time you start
the server, it may fail. In that case, reboot your computer, and the server
should succeed.

There is more detail about these steps in the following sections. Please
read those sections before proceeding.

**NOTE: **You may run a single micro-controller or all simultaneously on a single
computer, but only a single instance of a microcontroller may be run at a time.
For example,
you may run a Raspberry Pi and an Arduino simultaneously, and use one to control the
other. However, you may not run two of the same type of controllers at the same.

Running
two boards that use a serial link is an advanced and experimental feature and not recommended nor
officially supported. An example would be running
an Arduino and a Picoboard on the same computer at the same time.
If you wish to run two boards that use a serial link, you may have to manually specify 
the COM port for one of the boards. This is done by using 
the -c option in the launcher. For example, to start the Picoboard extension 
forcing it to use COM7, you would start the launcher with:

```bash
 s3p -c com7
```



<br> <br> <br>


Copyright (C) 2019-2020 Alan Yorinks All Rights Reserved
