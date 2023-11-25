from microbit import *
from neopixel import NeoPixel
import kitronic
from math import floor

num_pixels = 60
marker_colour = [0x0F, 0x00, 0x00]  # Hex color - red, green and blue
seconds_colour = [0x0F, 0x0F, 0x0F]
hours_am_colour = [0x00, 0x07, 0x0f]
hours_pm_colour = [0x00, 0x00, 0x17]
minutes_colour = [0x00, 0x0F, 0x00]

ring = NeoPixel(pin8, num_pixels)
rtc = kitronic.KitronikRTC()

def setup():

    # ring.show()              # actually display it
    rtc.setTime(23,58,50)

def markers():
    markers = (0,5,10,15,20,25,30,35,40,45,50,55)
    for i in markers:
        ring[i] = marker_colour

def clear_ring():
    for i in range(num_pixels):
        ring[i]=[0x00,0x00,0x00]
    
def tick(time):
    seconds_led = time[2]
    minutes_led = time[1]
    hours_led, pm = calc_hour_led(time[0], time[1])
    clear_ring()
    markers()
    if pm == 1:
        ring[hours_led]=hours_pm_colour
    else:
        ring[hours_led]=hours_am_colour
    ring[minutes_led]=minutes_colour
    ring[seconds_led]=seconds_colour
    ring.show()

def calc_hour_led(hour, minute):
    if hour >= 12:
        return ((hour-12)*5+floor(minute/12),1)
    
    print(hour)
    print(floor(minute/12))
    return (hour*5+floor(minute/12),0)

def check_time():
    rtc.readValue()
    return (rtc.currentHours, rtc.currentMinutes, rtc.currentSeconds)

def main():
    time_now = check_time()
    while True:
        if time_now != check_time():
            time_now = check_time()
            tick(time_now)



setup()
main()

