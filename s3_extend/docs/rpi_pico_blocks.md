## The Raspberry Pi Pico Blocks

![](./images/rpi_pico_blocks.png)

The blocks consist of a set of rectangular command blocks and 
rounded reporter blocks.

### Command Blocks

#### Write Digital
This block allows you to select a pin and set its output to either 1 or 0. 
It has two 
parameters. The first is a drop-down list of valid
PINs. The second parameter is a drop-down list that 
allows you to select either 0 or 1.

**NOTE:** Pin 25 controls the board LED.

#### Write PWM
This block allows you to select a pin and set its PWM output to a
value between 0 and 100%. It has two parameters. The first is a
drop-down list of valid PINs. The second parameter allows you to fill in
a PWM value. If you use a PWM value of less than 0, it will be internally set to 0.
If 
you set the value to greater than 100, it will be set
to 100.

**NOTE:** Pin 25 controls the board LED.

#### Write Servo
This block allows you to control the angle of a servo motor. It contains
two parameters. The first is a
drop-down list of valid PINs. The second specifies
the angle in degrees. The value is limited to the range of 0 to 180.

### Reporter Blocks

#### Read Digital
This block allows you to read the current state of a digital input pin and
reports the
raw input value as either zero or one.

The internal pull-up resistor for the pin is automatically enabled when using
this block.

#### Read Analog
This block allows you to read the current state of an analog input pin identified
by its ADC number.

| ADC Number |   GPIO Pin Number  |
|:----------:|:------------------:|
|      0     |         26         |
|      1     |         27         |
|      2     |         28         |
|      3     | Temperature Sensor |


It has one parameter, a drop-down list containing all the ADC Pins.
It reports a value between 0 and 4095. 

#### Read Sonar
This block enables you to connect an HC-SR04-type device. It has two 
parameters, both 
of which contain a drop-down list of valid PINs. The
first parameter allows you to select a trigger pin, and the second an
echo pin. It returns the measured distance in centimeters.
 
 
