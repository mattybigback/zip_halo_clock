# Zip Halo HD Clock

### RGB digitgal/analogue clock written in Micropython for the BBC Micro:bit

![Picture of device working](https://github.com/mattybigback/zip_halo_clock/blob/main/Images/Clock.png?raw=true)

[Kitronik ZIP Halo HD for the BBC micro:bit](https://kitronik.co.uk/products/5672-kitronik-zip-halo-hd-for-microbit)

## Setup

Download the latest hex file from the [releases page](https://github.com/mattybigback/zip_halo_clock/releases) and copy it to your micro:bit

## Usage

### Clock hands
* Seconds - white
* Minutes - green
* Hours - cyan (AM) or blue (PM)

The "hands" act like the real hands of an analogue clock. The hour hand moves forward by one place every 12 minutes. When more than one hand is on the same space the lowest value hand takes precedence, so at 13:05:05 LED number 5 will be white, at 13:05:06 it will be green at at 13:06 it will be blue.

### Menu

To enter the menu, press and hold buttons A and B for 2-3 seconds. Press button a to move to the next page, press (and hold) button b to make changes to the setting.

#### Page 1 - T
Turn on or off audible ticking.

#### Page 2 - H
Set the hour hand.

#### Page 3 - M
Set the minute hand.

#### Page 4 - S
Set the second hand.

#### Page 5
Exits menu and saves settings

## Notes on the code

The micro:bit has limited resources, so the code has been minified in order to make it fit. This means that variable names are not especially descriptive. It also means that there is not enough space to add a menu option to set the brightness of the LEDs. This can be set by changing BRT to a value between 0 and 4.

More features could be added if the code was reweritten in C++ using Arduino, but because of a bug in the Adafruit NeoPixel library I was unable to get the NeoPixel library to work on pin P8. This has been rasied as an [issue](https://github.com/adafruit/Adafruit_NeoPixel/issues/374), so hopefully someone smarter than me can find the cause and implement a fix.