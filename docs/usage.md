## An Overview Of Using The OneGPIO Extensions

Now that all the necessary software is installed both on your computer
and your physical computing device, it is time to try things out.

Here is a brief recommended procedure for using Scratch 3 with your
physical computing projects:

**Step 1:** With the power disconnected from your micro-controller, attach
the sensors and actuators to the micro-controller. ***Never*** add or
remove sensors or actuators with power applied - you may permanently
damage your micro-controller.
   
**Step 2:** Apply power to the micro-controller.

**Step 3:** Start the OneGPIO server code by opening a terminal window
for each microcontroller you wish to use and then enter the command for
the specific micro-controller:
   
   * **s3a** - for the Arduino
*    **s3e** - for the ESP-8266
*  **s3p** - for the Picoboard
   * **s3r** - for the Raspberry Pi
   
   Note: You may run a single micro-controller or all simultaneously,
   but only one instance of a micro-controller at a time. For example,
   you may run a Raspberry Pi and an Arduino, and use one to control the
   other, but you cannot run two of the same type of controller.
   
**Step 4:** Start Scratch 3, select an extension, and create and run
your Scratch scripts. If you are using the ESP-8266 Extension, when
Scratch is connected to the ESP-8266 by using the **ESP-8266 Connect IP Address** block, the red LED on the ESP-8266
NodeMCU is extinguished, indicating a successful connection.

**Step 5:** To power down, dismiss the OneGPIO server by going to the
window opened in step 3 and pressing Control-C. You may need to do this
twice. Finally, dismiss the Web Browser tab running
Scratch 3.


There is more detail about these steps in the following sections. Please
read those sections before proceeding.

<br> <br> <br>


Copyright (C) 2019 Alan Yorinks All Rights Reserved
