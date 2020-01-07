# The Circuit Playground Express Blocks

The blocks consist of a set of **HAT** blocks that have a bump at the left top,
**boolean** blocks that have pointed ends, **reporter** blocks that are rounded in shape,
and **command** blocks that are rectangular in shape.

## HAT Blocks

HAT blocks test for a specific condition. When that condition is met for
the first time, all of the blocks under the HAT block execute.

### When BUTTON Switch Is Pressed/Released
<img src="../images/cpx_hat_when_a.png" >


This block allows you to be notified when either button switch A or B, and the button is
either pressed or released.

### When SLIDE Switch Is Moved Left/Right
<img src="../images/cpx_hat_when_slide.png" >

This block executes when the slide switch moves to the selected position.

### When CPX Position is TILT_POSITION
<img src="../images/cpx_hat_when_position.png" >

This block executes when the Playground Express tilt position changes to
Flat, Up, Down, Left or Right.
















For example, ***When Light > 15***.

If the result of the comparison is TRUE, then all of the blocks below
this block are executed once.

### When Button Is Pressed
When the Picoboard button is pressed, all of the blocks below this block
are executed once.

### When The Selected SENSOR Value Is Within A Range
This block uses the current value of the selected sensor to check if its
value is within the specified range. If it is, then all of the blocks
below this block are executed once.

## Boolean Blocks

Boolean blocks test for a specific condition and return either True or False.

### Is Button Pressed
When the button is pressed, this blocks returns True. If the button is
not pressed, it returns FALSE.

### Is SENSOR Less Or Greater Than A Value
This block allows you to select a sensor type, a comparison type, and a
value for the comparison. It returns TRUE when the comparison is true
and FALSE when the comparison is false.

## Reporter Blocks

Reporter blocks retrieve the current value for a selected sensor.

### SENSOR Current Value
This block reports the current value of the selected sensor.

### Convert SENSOR To A Specified Range
This block scales the current value for the selected sensor and to be
within the specified range. So, for example, if the Slider is set to 100
and the range is set to -240 to 240, this block will return 240. If the
Slider is set to 50, this block will return 0, and if the Slider is set
to 0, this block will return -240.


 <br> <br> <br>


Copyright (C) 2019-2020 Alan Yorinks All Rights Reserved
